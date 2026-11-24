#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "upstream/usque-android/android/usque-vpn/app/src/main"

def read(p):
    return (ROOT / p).read_text(encoding="utf-8")

def write(p, s):
    (ROOT / p).write_text(s, encoding="utf-8")

write("res/values/strings.xml", '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">JianxianAPP Warp</string>
    <string name="app_version">版本 1.1.0</string>
</resources>
''')

layout = read("res/layout/activity_main.xml")
for old, new in [
    ('android:text="Usque VPN"', 'android:text="JianxianAPP Warp"'),
    ('android:text="Status"', 'android:text="连接状态"'),
    ('android:text="Disconnected"', 'android:text="未连接"'),
    ('android:text="Your IP Address"', 'android:text="WARP 分配的 IP 地址"'),
    ('android:text="Not registered"', 'android:text="尚未注册"'),
    ('android:text="SNI: www.visa.cn"', 'android:text="SNI：Cloudflare 系统默认"'),
    ('android:text="Endpoint: 162.159.198.1"', 'android:text="连接节点：默认节点"'),
    ('android:text="⚙ Settings"', 'android:text="测速优选 IP"'),
    ('android:text="Connect"', 'android:text="连接"'),
    ('android:text="Powered by usque"', 'android:text="JianxianAPP Warp · MASQUE 核心基于 usque"'),
]:
    layout = layout.replace(old, new)

# Replace settings button id with the speed-test button id.
layout = layout.replace('android:id="@+id/settings_button"', 'android:id="@+id/ip_list_button"')
footer = '''    <!-- Footer -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="JianxianAPP Warp · MASQUE 核心基于 usque"
        android:textSize="12sp"
        android:textColor="#555555"
        android:layout_marginTop="32dp" />'''
replacement = footer + '''
    <TextView
        android:id="@+id/version_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="版本 1.1.0"
        android:textSize="12sp"
        android:textColor="#888888"
        android:layout_marginTop="8dp" />
    <TextView
        android:id="@+id/github_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="GitHub：github.com/mengxianbo"
        android:textSize="12sp"
        android:textColor="#64b5f6"
        android:clickable="true"
        android:focusable="true"
        android:layout_marginTop="6dp" />'''
if 'id="@+id/github_text"' not in layout:
    layout = layout.replace(footer, replacement)
write("res/layout/activity_main.xml", layout)

write("res/layout/dialog_settings.xml", '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="20dp">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="SNI 使用 Cloudflare MASQUE 系统默认值。请通过“测速优选 IP”测试并选择可用节点。"
        android:textSize="14sp" />
</LinearLayout>
''')

kotlin = r'''package com.abobo.usquevpn

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.net.VpnService
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.core.content.ContextCompat
import usqueandroid.Usqueandroid
import java.util.concurrent.Executors

class MainActivity : Activity() {
    companion object {
        private const val VPN_REQUEST_CODE = 1001
        private const val NOTIFICATION_REQUEST_CODE = 1002
        private const val PREFS_NAME = "JianxianWarpPrefs"
        private const val KEY_SELECTED_ENDPOINT = "selected_endpoint"
        private const val APP_VERSION = "1.1.0"
        private const val AUTHOR_URL = "https://github.com/mengxianbo"
        private val BUILT_IN_ENDPOINTS = listOf("162.159.198.2:443", "162.159.198.10:443")
    }

    private data class ProbeResult(val endpoint: String, val latencyMs: Long?, val error: String?)
    private lateinit var prefs: SharedPreferences
    private lateinit var statusText: TextView
    private lateinit var connectButton: Button
    private lateinit var ipInfoText: TextView
    private lateinit var ipListButton: Button
    private lateinit var sniText: TextView
    private lateinit var endpointText: TextView
    private lateinit var versionText: TextView
    private lateinit var githubText: TextView
    private var registeredEndpoint = ""
    private var probeResults: List<ProbeResult> = emptyList()
    private val probeExecutor = Executors.newSingleThreadExecutor()
    private val uiHandler = Handler(Looper.getMainLooper())
    private val refreshUi = object : Runnable {
        override fun run() {
            updateUI()
            if (UsqueVpnService.isRunning) uiHandler.postDelayed(this, 500)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        statusText = findViewById(R.id.status_text)
        connectButton = findViewById(R.id.connect_button)
        ipInfoText = findViewById(R.id.ip_info_text)
        ipListButton = findViewById(R.id.ip_list_button)
        sniText = findViewById(R.id.sni_text)
        endpointText = findViewById(R.id.endpoint_text)
        versionText = findViewById(R.id.version_text)
        githubText = findViewById(R.id.github_text)
        loadSavedSettings()
        versionText.text = "版本 $APP_VERSION"
        githubText.setOnClickListener {
            startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse(AUTHOR_URL)))
        }
        requestNotificationPermissionIfNeeded()
        connectButton.setOnClickListener {
            if (UsqueVpnService.isRunning) stopVpn() else startVpn()
        }
        ipListButton.setOnClickListener { runEndpointSpeedTest() }
        updateUI()
    }

    override fun onResume() {
        super.onResume()
        uiHandler.removeCallbacks(refreshUi)
        uiHandler.post(refreshUi)
    }

    override fun onPause() {
        uiHandler.removeCallbacks(refreshUi)
        super.onPause()
    }

    override fun onDestroy() {
        probeExecutor.shutdownNow()
        super.onDestroy()
    }

    private fun requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), NOTIFICATION_REQUEST_CODE)
        }
    }

    private fun loadSavedSettings() {
        // Ignore legacy custom SNI settings; empty selects the core's Cloudflare default.
        Usqueandroid.setSNI("")
        Usqueandroid.setEndpoint(prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: "")
    }

    private fun runEndpointSpeedTest() {
        if (UsqueVpnService.isRunning) {
            Toast.makeText(this, "请先断开 VPN，再进行节点测速", Toast.LENGTH_SHORT).show()
            return
        }
        val configPath = "${filesDir.absolutePath}/config.json"
        if (!Usqueandroid.isRegistered(configPath)) {
            Toast.makeText(this, "请先连接一次以完成 WARP 注册，再进行测速", Toast.LENGTH_LONG).show()
            return
        }
        val candidates = (BUILT_IN_ENDPOINTS + Usqueandroid.getDefaultEndpoint(configPath))
            .map { it.trim() }.filter { it.isNotEmpty() }.distinct()
        if (candidates.isEmpty()) {
            Toast.makeText(this, "当前没有可测速的候选 IP", Toast.LENGTH_SHORT).show()
            return
        }
        ipListButton.isEnabled = false
        val progress = AlertDialog.Builder(this)
            .setTitle("正在测速优选 IP")
            .setMessage("逐个进行真实 MASQUE / QUIC 隧道握手测试，请稍候…")
            .setNegativeButton("后台继续", null)
            .create()
        progress.show()
        probeExecutor.execute {
            val results = candidates.map { endpoint ->
                val raw = try {
                    Usqueandroid.testEndpoint(configPath, endpoint, 5000L)
                } catch (t: Throwable) {
                    "ERR:${t.message ?: "测速失败"}"
                }
                if (raw.startsWith("OK:")) ProbeResult(endpoint, raw.removePrefix("OK:").toLongOrNull(), null)
                else ProbeResult(endpoint, null, raw.removePrefix("ERR:").ifBlank { "握手失败" })
            }.sortedWith(compareBy<ProbeResult> { it.latencyMs == null }.thenBy { it.latencyMs ?: Long.MAX_VALUE })
            uiHandler.post {
                progress.dismiss()
                ipListButton.isEnabled = !UsqueVpnService.isRunning
                probeResults = results
                showProbeResults()
            }
        }
    }

    private fun showProbeResults() {
        if (probeResults.isEmpty()) return
        val selected = prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: ""
        val labels = probeResults.map { result ->
            val mark = if (result.endpoint == selected) "  ✓ 当前使用" else ""
            if (result.latencyMs != null) "${result.endpoint}    ${result.latencyMs} ms$mark"
            else "${result.endpoint}    不可用$mark"
        }.toTypedArray()
        val count = probeResults.count { it.latencyMs != null }
        AlertDialog.Builder(this)
            .setTitle("测速结果（成功 $count/${probeResults.size}）")
            .setItems(labels) { _, which ->
                val result = probeResults.getOrNull(which) ?: return@setItems
                if (result.latencyMs == null) {
                    Toast.makeText(this, "该节点握手失败，不能选择", Toast.LENGTH_SHORT).show()
                    return@setItems
                }
                if (UsqueVpnService.isRunning) {
                    Toast.makeText(this, "请先断开 VPN，再切换节点", Toast.LENGTH_SHORT).show()
                    return@setItems
                }
                prefs.edit().putString(KEY_SELECTED_ENDPOINT, result.endpoint).apply()
                Usqueandroid.setEndpoint(result.endpoint)
                Toast.makeText(this, "已保存节点：${result.endpoint}", Toast.LENGTH_SHORT).show()
                updateUI()
            }
            .setPositiveButton("重新测速") { _, _ -> runEndpointSpeedTest() }
            .setNegativeButton("关闭", null)
            .show()
    }

    private fun startVpn() {
        Usqueandroid.setSNI("")
        Usqueandroid.setEndpoint(prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: "")
        val intent = VpnService.prepare(this)
        if (intent != null) startActivityForResult(intent, VPN_REQUEST_CODE) else onVpnPermissionGranted()
    }

    private fun stopVpn() {
        UsqueVpnService.stop()
        startService(Intent(this, UsqueVpnService::class.java).apply { action = UsqueVpnService.ACTION_DISCONNECT })
        updateUI()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != VPN_REQUEST_CODE) return
        if (resultCode == RESULT_OK) onVpnPermissionGranted()
        else Toast.makeText(this, "VPN 权限未授予", Toast.LENGTH_SHORT).show()
    }

    private fun onVpnPermissionGranted() {
        val intent = Intent(this, UsqueVpnService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) ContextCompat.startForegroundService(this, intent)
        else startService(intent)
        uiHandler.removeCallbacks(refreshUi)
        uiHandler.post(refreshUi)
    }

    private fun updateUI() {
        val configPath = "${filesDir.absolutePath}/config.json"
        if (UsqueVpnService.isRunning) {
            if (UsqueVpnService.isConnected) {
                statusText.text = "已连接"
                statusText.setTextColor(getColor(android.R.color.holo_green_dark))
            } else {
                statusText.text = "正在连接…"
                statusText.setTextColor(getColor(android.R.color.holo_orange_dark))
            }
            connectButton.text = "断开连接"
            ipListButton.isEnabled = false
        } else {
            statusText.text = "未连接"
            statusText.setTextColor(getColor(android.R.color.holo_red_dark))
            connectButton.text = "连接"
            ipListButton.isEnabled = true
        }
        if (!UsqueVpnService.isRunning) {
            if (Usqueandroid.isRegistered(configPath)) {
                val ipv4 = Usqueandroid.getAssignedIPv4(configPath)
                val ipv6 = Usqueandroid.getAssignedIPv6(configPath)
                ipInfoText.text = "IPv4：$ipv4\nIPv6：$ipv6"
                registeredEndpoint = Usqueandroid.getDefaultEndpoint(configPath)
            } else {
                ipInfoText.text = "尚未注册"
            }
        }
        val selected = prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: ""
        sniText.text = "SNI：Cloudflare 系统默认"
        endpointText.text = "连接节点：" + selected.ifEmpty { registeredEndpoint.ifEmpty { "注册后自动获取" } }
    }
}
'''
write("kotlin/com/abobo/usquevpn/MainActivity.kt", kotlin)

go = ROOT.parents[3] / "usque_android.go"
source = go.read_text(encoding="utf-8")
source = source.replace('customSNI      = "www.visa.cn" // Default SNI for censorship circumvention.', 'customSNI      = "" // Empty selects the Cloudflare MASQUE default SNI.')
source = source.replace('customSNI = "www.visa.cn"', 'customSNI = ""')
source = source.replace('return "1.0.4-android"', 'return "1.1.0-android"')
probe = r'''
// TestEndpoint performs a real MASQUE/QUIC Connect-IP handshake using the
// registered account's pinned peer key, without creating a TUN or VPN session.
func TestEndpoint(configPath string, endpointOverride string, timeoutMs int64) string {
    started := time.Now()
    if timeoutMs <= 0 { timeoutMs = 5000 }
    if err := config.LoadConfig(configPath); err != nil { return fmt.Sprintf("ERR:load config: %v", err) }
    privKey, err := config.AppConfig.GetEcPrivateKey()
    if err != nil { return fmt.Sprintf("ERR:private key: %v", err) }
    peerPubKey, err := config.AppConfig.GetEcEndpointPublicKey()
    if err != nil { return fmt.Sprintf("ERR:peer public key: %v", err) }
    cert, err := internal.GenerateCert(privKey, &privKey.PublicKey)
    if err != nil { return fmt.Sprintf("ERR:client certificate: %v", err) }
    tlsConfig, err := api.PrepareTlsConfig(privKey, peerPubKey, cert, internal.ConnectSNI, false)
    if err != nil { return fmt.Sprintf("ERR:TLS config: %v", err) }
    endpoint, err := parseEndpoint(endpointOverride)
    if err != nil { return fmt.Sprintf("ERR:endpoint: %v", err) }
    ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeoutMs)*time.Millisecond)
    defer cancel()
    udpConn, tr, ipConn, rsp, err := api.ConnectTunnel(ctx, tlsConfig,
        internal.DefaultQuicConfig(30*time.Second, 1242), internal.ConnectURI, endpoint, false)
    if ipConn != nil { defer ipConn.Close() }
    if tr != nil { defer tr.Close() }
    if udpConn != nil { defer udpConn.Close() }
    if err != nil { return fmt.Sprintf("ERR:%v", err) }
    if rsp == nil { return "ERR:missing Connect-IP response" }
    if rsp.StatusCode != 200 { return fmt.Sprintf("ERR:Connect-IP status %s", rsp.Status) }
    return fmt.Sprintf("OK:%d", time.Since(started).Milliseconds())
}

'''
if "func TestEndpoint(" not in source:
    source = source.replace("// GetVersion returns the Android wrapper version.", probe + "// GetVersion returns the Android wrapper version.")
go.write_text(source, encoding="utf-8")

service = read("kotlin/com/abobo/usquevpn/UsqueVpnService.kt")
for old, new in [
    ('"Usque WARP VPN"', '"JianxianAPP Warp"'),
    ('"Connecting…"', '"正在连接…"'),
    ('"Connected"', '"已连接"'),
    ('"Reconnecting…"', '"正在重连…"'),
    ('"Error"', '"连接错误"'),
    ('"Usque VPN"', '"JianxianAPP Warp"'),
    ('"Usque MASQUE VPN status"', '"JianxianAPP Warp 连接状态"'),
]:
    service = service.replace(old, new)
write("kotlin/com/abobo/usquevpn/UsqueVpnService.kt", service)

# Keep the Android package metadata aligned with the visible app version.
gradle = ROOT.parents[2] / "app/build.gradle.kts"
if gradle.exists():
    build = gradle.read_text(encoding="utf-8")
    build = build.replace("versionCode = 4", "versionCode = 5")
    build = build.replace('versionName = "1.0.4"', 'versionName = "1.1.0"')
    gradle.write_text(build, encoding="utf-8")

print("Applied JianxianAPP Warp 1.1.0 branding, saved MASQUE endpoint selection, QUIC handshake speed tests, and fixed default SNI.")
