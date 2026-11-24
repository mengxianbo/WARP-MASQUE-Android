#!/usr/bin/env python3
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "upstream/usque-android/android/usque-vpn/app/src/main"
def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value, encoding="utf-8")
def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

write("res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources><string name="app_name">Hide Wi-Fi</string><string name="app_version">版本 1.2.0</string></resources>
""")

write("res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
 android:layout_width="match_parent" android:layout_height="match_parent" android:background="#101827" android:fillViewport="true">
 <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical"
  android:gravity="center_horizontal" android:padding="22dp">
  <ImageView android:layout_width="112dp" android:layout_height="112dp" android:src="@drawable/ic_compass" android:layout_marginTop="18dp"/>
  <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Hide Wi-Fi"
   android:textSize="28sp" android:textStyle="bold" android:textColor="#ffffff" android:layout_marginTop="10dp"/>
  <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Cloudflare WARP · MASQUE"
   android:textSize="14sp" android:textColor="#9ca3af" android:layout_marginTop="5dp" android:layout_marginBottom="24dp"/>
  <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical"
   android:padding="18dp" android:background="@drawable/card_background">
   <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="WARP VPN 状态"
    android:textColor="#9ca3af" android:textSize="12sp"/>
   <TextView android:id="@+id/status_text" android:layout_width="wrap_content" android:layout_height="wrap_content"
    android:text="未连接" android:textColor="#ff7777" android:textSize="23sp" android:textStyle="bold" android:layout_marginTop="5dp"/>
   <TextView android:id="@+id/ip_info_text" android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="尚未注册" android:textColor="#e5e7eb" android:textSize="13sp" android:layout_marginTop="12dp"/>
   <TextView android:id="@+id/endpoint_text" android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="连接节点：注册后自动获取" android:textColor="#9ca3af" android:textSize="12sp" android:layout_marginTop="8dp"/>
  </LinearLayout>
  <Button android:id="@+id/connect_button" android:layout_width="match_parent" android:layout_height="54dp"
   android:text="连接 WARP VPN" android:textSize="16sp" android:textStyle="bold" android:textColor="#ffffff"
   android:background="@drawable/button_background" android:layout_marginTop="16dp"/>
  <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical"
   android:padding="18dp" android:background="@drawable/card_background" android:layout_marginTop="16dp">
   <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="局域网共享代理"
    android:textColor="#ffffff" android:textSize="17sp" android:textStyle="bold"/>
   <TextView android:id="@+id/proxy_info_text" android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="代理未启动。启动后点击此处可复制连接信息。" android:textColor="#d1d5db" android:textSize="13sp"
    android:layout_marginTop="10dp" android:clickable="true" android:focusable="true"/>
   <Button android:id="@+id/proxy_settings_button" android:layout_width="match_parent" android:layout_height="48dp"
    android:text="设置 HTTP 代理账号 / 密码" android:textColor="#ffffff"
    android:background="@drawable/button_secondary_background" android:layout_marginTop="12dp"/>
   <Button android:id="@+id/proxy_button" android:layout_width="match_parent" android:layout_height="50dp"
    android:text="启动 HTTP 代理（端口 6668）" android:textColor="#ffffff"
    android:background="@drawable/button_secondary_background" android:layout_marginTop="8dp"/>
   <TextView android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="HTTP 代理支持 HTTP 和 HTTPS CONNECT（TCP）。可手动设置账号密码，也可关闭认证；仅允许本地局域网地址连接。"
    android:textColor="#9ca3af" android:textSize="11sp" android:layout_marginTop="8dp"/>
   <TextView android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="WebRTC 提醒：HTTP 代理不转发 UDP / QUIC，不能单独防止 WebRTC 泄漏；需在客户端设备启用 VPN 或禁用 WebRTC / QUIC。"
    android:textColor="#fbbf24" android:textSize="11sp" android:layout_marginTop="7dp"/>
  </LinearLayout>
  <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
   android:text="Hide Wi-Fi · MASQUE 核心基于 usque" android:textSize="11sp" android:textColor="#6b7280" android:layout_marginTop="24dp"/>
  <TextView android:id="@+id/version_text" android:layout_width="wrap_content" android:layout_height="wrap_content"
   android:text="版本 1.2.0" android:textSize="12sp" android:textColor="#9ca3af" android:layout_marginTop="6dp"/>
  <TextView android:id="@+id/github_text" android:layout_width="wrap_content" android:layout_height="wrap_content"
   android:text="GitHub：github.com/mengxianbo" android:textSize="12sp" android:textColor="#60a5fa"
   android:clickable="true" android:focusable="true" android:layout_marginTop="6dp" android:layout_marginBottom="24dp"/>
 </LinearLayout>
</ScrollView>
""")

write("res/drawable/ic_compass.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="120dp" android:height="120dp"
 android:viewportWidth="120" android:viewportHeight="120">
 <path android:fillColor="#172554" android:pathData="M60,4 A56,56 0,1 0,60.01 4 Z"/>
 <path android:strokeColor="#93c5fd" android:strokeWidth="3" android:fillColor="#1e3a8a"
  android:pathData="M60,12 A48,48 0,1 0,60.01 12 Z"/>
 <path android:fillColor="#dbeafe" android:pathData="M60,18 L65,55 L60,60 L55,55 Z"/>
 <path android:fillColor="#f97316" android:pathData="M60,102 L55,65 L60,60 L65,65 Z"/>
 <path android:fillColor="#ffffff" android:pathData="M60,39 L80,80 L60,68 L40,80 Z"/>
 <path android:fillColor="#f97316" android:pathData="M60,39 L60,68 L40,80 Z"/>
 <path android:fillColor="#ffffff" android:pathData="M57,8 L63,8 L60,17 Z M57,112 L63,112 L60,103 Z M8,57 L8,63 L17,60 Z M112,57 L112,63 L103,60 Z"/>
 <path android:fillColor="#0f172a" android:pathData="M60,55 A5,5 0,1 0,60.01 55 Z"/>
</vector>
""")

write("kotlin/com/abobo/usquevpn/MainActivity.kt", r'''package com.abobo.usquevpn

import android.Manifest
import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.net.Uri
import android.net.VpnService
import android.net.wifi.WifiManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.format.Formatter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.text.InputType
import android.app.AlertDialog
import android.widget.Toast
import androidx.core.content.ContextCompat
import usqueandroid.Usqueandroid
import java.security.SecureRandom

class MainActivity : Activity() {
    companion object {
        private const val VPN_REQUEST_CODE = 1001
        private const val NOTIFICATION_REQUEST_CODE = 1002
        private const val PREFS_NAME = "JianxianWarpPrefs"
        private const val KEY_SELECTED_ENDPOINT = "selected_endpoint"
        private const val KEY_PROXY_USER = "proxy_user"
        private const val KEY_PROXY_PASS = "proxy_pass"
        private const val KEY_PROXY_AUTH = "proxy_auth_enabled"
        private const val APP_VERSION = "1.2.0"
        private const val AUTHOR_URL = "https://github.com/mengxianbo"
        private const val PROXY_PORT = 6668
    }
    private lateinit var prefs: SharedPreferences
    private lateinit var statusText: TextView
    private lateinit var connectButton: Button
    private lateinit var ipInfoText: TextView
    private lateinit var endpointText: TextView
    private lateinit var proxyButton: Button
    private lateinit var proxySettingsButton: Button
    private lateinit var proxyInfoText: TextView
    private lateinit var versionText: TextView
    private lateinit var githubText: TextView
    private var registeredEndpoint = ""
    private val uiHandler = Handler(Looper.getMainLooper())
    private val refreshUi = object : Runnable {
        override fun run() {
            updateUI()
            uiHandler.postDelayed(this, 1000)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        statusText = findViewById(R.id.status_text)
        connectButton = findViewById(R.id.connect_button)
        ipInfoText = findViewById(R.id.ip_info_text)
        endpointText = findViewById(R.id.endpoint_text)
        proxyButton = findViewById(R.id.proxy_button)
        proxySettingsButton = findViewById(R.id.proxy_settings_button)
        proxyInfoText = findViewById(R.id.proxy_info_text)
        versionText = findViewById(R.id.version_text)
        githubText = findViewById(R.id.github_text)
        Usqueandroid.setSNI("")
        Usqueandroid.setEndpoint(prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: "")
        versionText.text = "版本 " + APP_VERSION
        githubText.setOnClickListener { startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(AUTHOR_URL))) }
        proxyInfoText.setOnClickListener { copyProxyInfo() }
        requestNotificationPermissionIfNeeded()
        connectButton.setOnClickListener { if (UsqueVpnService.isRunning) stopVpn() else startVpn() }
        proxyButton.setOnClickListener { if (ProxyService.isRunning) stopProxy() else startProxy() }
        proxySettingsButton.setOnClickListener { showProxySettings() }
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
    private fun requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), NOTIFICATION_REQUEST_CODE)
        }
    }
    private fun ensureProxyDefaults() {
        if (!prefs.contains(KEY_PROXY_AUTH)) prefs.edit().putBoolean(KEY_PROXY_AUTH, true).apply()
        if (!prefs.contains(KEY_PROXY_USER)) prefs.edit().putString(KEY_PROXY_USER, "").apply()
        if (!prefs.contains(KEY_PROXY_PASS)) prefs.edit().putString(KEY_PROXY_PASS, "").apply()
    }

    private fun showProxySettings() {
        ensureProxyDefaults()
        val box = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(48, 20, 48, 8) }
        val auth = android.widget.CheckBox(this).apply {
            text = "启用用户名和密码认证（建议开启）"
            isChecked = prefs.getBoolean(KEY_PROXY_AUTH, true)
        }
        val user = EditText(this).apply { hint = "代理用户名"; setSingleLine(true); setText(prefs.getString(KEY_PROXY_USER, "")) }
        val pass = EditText(this).apply {
            hint = "代理密码"; setSingleLine(true)
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            setText(prefs.getString(KEY_PROXY_PASS, ""))
        }
        box.addView(auth); box.addView(user); box.addView(pass)
        AlertDialog.Builder(this).setTitle("HTTP 代理设置")
            .setMessage("端口固定为 6668。关闭认证后，同一局域网内的设备无需账号密码。")
            .setView(box).setNegativeButton("取消", null)
            .setPositiveButton("保存") { _, _ ->
                val u = user.text.toString().trim()
                val p = pass.text.toString()
                if (auth.isChecked && (u.isBlank() || p.isBlank())) {
                    Toast.makeText(this, "开启认证时用户名和密码不能为空", Toast.LENGTH_LONG).show()
                    return@setPositiveButton
                }
                if (u.contains(":") || u.contains("\\r") || u.contains("\\n") || p.contains("\\r") || p.contains("\\n")) {
                    Toast.makeText(this, "用户名或密码包含不支持的字符", Toast.LENGTH_LONG).show()
                    return@setPositiveButton
                }
                prefs.edit().putBoolean(KEY_PROXY_AUTH, auth.isChecked).putString(KEY_PROXY_USER, u).putString(KEY_PROXY_PASS, p).apply()
                if (ProxyService.isRunning) stopProxy()
                Toast.makeText(this, "代理设置已保存", Toast.LENGTH_SHORT).show()
                updateUI()
            }.show()
    }
    private fun startProxy() {
        val configPath = filesDir.absolutePath + "/config.json"
        if (!Usqueandroid.isRegistered(configPath)) {
            Toast.makeText(this, "请先连接一次 WARP 完成注册，再启动共享代理", Toast.LENGTH_LONG).show()
            return
        }
        ensureProxyDefaults()
        val auth = prefs.getBoolean(KEY_PROXY_AUTH, true)
        val user = prefs.getString(KEY_PROXY_USER, "") ?: ""
        val pass = prefs.getString(KEY_PROXY_PASS, "") ?: ""
        if (auth && (user.isBlank() || pass.isBlank())) {
            Toast.makeText(this, "请先在代理设置中填写用户名和密码", Toast.LENGTH_LONG).show()
            showProxySettings()
            return
        }
        val intent = Intent(this, ProxyService::class.java)
        intent.putExtra(ProxyService.EXTRA_AUTH, auth)
        intent.putExtra(ProxyService.EXTRA_USERNAME, user)
        intent.putExtra(ProxyService.EXTRA_PASSWORD, pass)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) ContextCompat.startForegroundService(this, intent) else startService(intent)
    }
    private fun stopProxy() {
        startService(Intent(this, ProxyService::class.java).setAction(ProxyService.ACTION_STOP))
    }
    private fun copyProxyInfo() {
        if (!ProxyService.isRunning) {
            Toast.makeText(this, "请先启动代理", Toast.LENGTH_SHORT).show()
            return
        }
        ensureProxyDefaults()
        val auth = prefs.getBoolean(KEY_PROXY_AUTH, true)
        val info = "HTTP " + getWifiIpAddress() + ":" + PROXY_PORT +
            if (auth) "\n用户名：" + prefs.getString(KEY_PROXY_USER, "") + "\n密码：" + prefs.getString(KEY_PROXY_PASS, "")
            else "\n无需认证"
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("Hide Wi-Fi HTTP Proxy", info))
        Toast.makeText(this, "代理连接信息已复制", Toast.LENGTH_SHORT).show()
    }
    private fun getWifiIpAddress(): String {
        return try {
            val wifi = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
            val ip = wifi.connectionInfo.ipAddress
            if (ip == 0) "请连接 Wi-Fi" else Formatter.formatIpAddress(ip)
        } catch (_: Exception) { "请连接 Wi-Fi" }
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
    }
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != VPN_REQUEST_CODE) return
        if (resultCode == RESULT_OK) onVpnPermissionGranted()
        else Toast.makeText(this, "VPN 权限未授予", Toast.LENGTH_SHORT).show()
    }
    private fun onVpnPermissionGranted() {
        val intent = Intent(this, UsqueVpnService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) ContextCompat.startForegroundService(this, intent) else startService(intent)
    }
    private fun updateUI() {
        val configPath = filesDir.absolutePath + "/config.json"
        if (UsqueVpnService.isRunning) {
            statusText.text = if (UsqueVpnService.isConnected) "已连接" else "正在连接…"
            statusText.setTextColor(getColor(if (UsqueVpnService.isConnected) android.R.color.holo_green_dark else android.R.color.holo_orange_dark))
            connectButton.text = "断开 WARP VPN"
        } else {
            statusText.text = "未连接"
            statusText.setTextColor(getColor(android.R.color.holo_red_dark))
            connectButton.text = "连接 WARP VPN"
        }
        if (!UsqueVpnService.isRunning && Usqueandroid.isRegistered(configPath)) {
            ipInfoText.text = "WARP IPv4：" + Usqueandroid.getAssignedIPv4(configPath) +
                "\nWARP IPv6：" + Usqueandroid.getAssignedIPv6(configPath)
            registeredEndpoint = Usqueandroid.getDefaultEndpoint(configPath)
        } else if (!UsqueVpnService.isRunning) ipInfoText.text = "尚未注册"
        val selected = prefs.getString(KEY_SELECTED_ENDPOINT, "") ?: ""
        endpointText.text = "连接节点：" + selected.ifEmpty { registeredEndpoint.ifEmpty { "注册后自动获取" } }
        ensureProxyDefaults()
        val authEnabled = prefs.getBoolean(KEY_PROXY_AUTH, true)
        proxySettingsButton.text = if (authEnabled) "HTTP 代理账号 / 密码设置（认证开启）" else "HTTP 代理账号 / 密码设置（认证关闭）"
        if (ProxyService.isRunning) {
            proxyButton.text = "停止 HTTP 代理"
            proxyInfoText.text = "HTTP 地址：" + getWifiIpAddress() + ":" + PROXY_PORT +
                if (authEnabled) "\n认证：已开启\n用户名：" + prefs.getString(KEY_PROXY_USER, "") + "\n密码：••••••••\n\n点击复制连接信息"
                else "\n认证：已关闭\n无需账号密码\n\n点击复制连接信息"
        } else {
            proxyButton.text = "启动 HTTP 代理（端口 6668）"
            proxyInfoText.text = "代理未启动。可先设置账号密码，再启动代理。"
        }
    }
}
''')

write("kotlin/com/abobo/usquevpn/ProxyService.kt", r'''package com.abobo.usquevpn

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket
import java.util.Base64
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean

class ProxyService : Service() {
    companion object {
        const val ACTION_STOP = "com.abobo.usquevpn.PROXY_STOP"
        const val EXTRA_USERNAME = "proxy_username"
        const val EXTRA_PASSWORD = "proxy_password"
        const val EXTRA_AUTH = "proxy_auth"
        private const val CHANNEL_ID = "hide_wifi_proxy"
        private const val NOTIFICATION_ID = 1002
        @Volatile var isRunning = false
            private set
    }
    private val running = AtomicBoolean(false)
    private val workers = Executors.newCachedThreadPool()
    private var server: ServerSocket? = null

    override fun onCreate() {
        super.onCreate()
        val channel = NotificationChannel(CHANNEL_ID, "Hide Wi-Fi HTTP 代理", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopProxy(); stopForeground(true); stopSelf()
            return START_NOT_STICKY
        }
        val launch = packageManager.getLaunchIntentForPackage(packageName)
        val pending = if (launch == null) null else PendingIntent.getActivity(this, 0, launch,
            PendingIntent.FLAG_UPDATE_CURRENT or if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0)
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_compass).setContentTitle("Hide Wi-Fi HTTP 代理")
            .setContentText("局域网 HTTP 代理监听端口 6668").setOngoing(true)
            .setCategory(NotificationCompat.CATEGORY_SERVICE).setContentIntent(pending).build()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE)
            startForeground(NOTIFICATION_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE)
        else startForeground(NOTIFICATION_ID, notification)
        if (running.get()) return START_NOT_STICKY
        val auth = intent?.getBooleanExtra(EXTRA_AUTH, true) ?: true
        val user = intent?.getStringExtra(EXTRA_USERNAME) ?: ""
        val pass = intent?.getStringExtra(EXTRA_PASSWORD) ?: ""
        if (auth && (user.isBlank() || pass.isBlank())) {
            stopForeground(true); stopSelf(); return START_NOT_STICKY
        }
        try {
            server = ServerSocket(6668, 64, InetAddress.getByName("0.0.0.0"))
            running.set(true); isRunning = true
            workers.execute {
                while (running.get()) {
                    try {
                        val client = server?.accept() ?: break
                        if (!isLanAddress(client.inetAddress)) client.close()
                        else workers.execute { handleClient(client, auth, user, pass) }
                    } catch (_: Exception) { if (!running.get()) break }
                }
            }
        } catch (_: Exception) { stopProxy(); stopForeground(true); stopSelf() }
        return START_NOT_STICKY
    }

    private fun isLanAddress(a: InetAddress): Boolean =
        a.isLoopbackAddress || a.isSiteLocalAddress || a.isLinkLocalAddress

    private fun handleClient(client: Socket, auth: Boolean, user: String, pass: String) {
        client.use { socket ->
            socket.soTimeout = 30000
            val input = BufferedInputStream(socket.getInputStream())
            val output = BufferedOutputStream(socket.getOutputStream())
            val header = java.io.ByteArrayOutputStream()
            var state = 0
            while (header.size() < 32768) {
                val b = input.read()
                if (b < 0) return
                header.write(b)
                state = when {
                    state == 0 && b == 13 -> 1
                    state == 1 && b == 10 -> 2
                    state == 2 && b == 13 -> 3
                    state == 3 && b == 10 -> 4
                    b == 13 -> 1
                    else -> 0
                }
                if (state == 4) break
            }
            if (state != 4) { respond(output, "431 Request Header Fields Too Large"); return }
            val lines = String(header.toByteArray(), Charsets.ISO_8859_1).split("\r\n")
            val parts = lines.firstOrNull()?.split(" ") ?: emptyList()
            if (parts.size < 3) { respond(output, "400 Bad Request"); return }
            val method = parts[0].uppercase()
            val target = parts[1]
            val authLine = lines.firstOrNull { it.startsWith("Proxy-Authorization:", true) }
            if (auth && !checkAuth(authLine?.substringAfter(":")?.trim(), user, pass)) {
                output.write("HTTP/1.1 407 Proxy Authentication Required\r\nProxy-Authenticate: Basic realm=\\"Hide Wi-Fi\\"\r\nConnection: close\r\nContent-Length: 0\r\n\r\n".toByteArray(Charsets.ISO_8859_1))
                output.flush(); return
            }
            val uri = if (method == "CONNECT") null else try { java.net.URI(target) } catch (_: Exception) { null }
            val host = if (method == "CONNECT") target.substringBeforeLast(":").removePrefix("[").removeSuffix("]")
                else uri?.host
            val port = if (method == "CONNECT") target.substringAfterLast(":", "443").toIntOrNull() ?: 443
                else if ((uri?.port ?: -1) > 0) uri!!.port else 80
            if (host.isNullOrBlank() || port !in 1..65535) { respond(output, "400 Bad Request"); return }
            val upstream = try { Socket(host, port).apply { soTimeout = 30000 } }
                catch (_: Exception) { respond(output, "502 Bad Gateway"); return }
            upstream.use { remote ->
                if (method == "CONNECT") {
                    output.write("HTTP/1.1 200 Connection Established\r\n\r\n".toByteArray(Charsets.ISO_8859_1))
                    output.flush()
                    socket.soTimeout = 0; remote.soTimeout = 0
                    val a = Thread { copyStream(input, remote.getOutputStream()) }
                    val b = Thread { copyStream(remote.getInputStream(), output) }
                    a.start(); b.join(30000); try { socket.close(); remote.close() } catch (_: Exception) {}; a.join(1000)
                } else {
                    if (uri == null || uri.scheme != "http") { respond(output, "400 Bad Request"); return }
                    val path = (uri.rawPath.ifEmpty { "/" }) + (if (uri.rawQuery != null) "?" + uri.rawQuery else "")
                    val req = StringBuilder().append(method).append(" ").append(path).append(" ").append(parts[2]).append("\r\n")
                    lines.drop(1).filter { it.isNotBlank() && !it.startsWith("Proxy-Authorization:", true) && !it.startsWith("Proxy-Connection:", true) }
                        .forEach { req.append(it).append("\r\n") }
                    req.append("Connection: close\r\n\r\n")
                    remote.getOutputStream().write(req.toString().toByteArray(Charsets.ISO_8859_1))
                    remote.getOutputStream().flush()
                    input.copyTo(remote.getOutputStream()); remote.getOutputStream().flush()
                    remote.getInputStream().copyTo(output); output.flush()
                }
            }
        }
    }

    private fun checkAuth(value: String?, user: String, pass: String): Boolean {
        if (value == null || !value.startsWith("Basic ", true)) return false
        val decoded = try { String(Base64.getDecoder().decode(value.substringAfter(" ").trim()), Charsets.UTF_8) }
            catch (_: Exception) { return false }
        return decoded == user + ":" + pass
    }

    private fun respond(out: BufferedOutputStream, status: String) {
        out.write(("HTTP/1.1 " + status + "\r\nConnection: close\r\nContent-Length: 0\r\n\r\n").toByteArray(Charsets.ISO_8859_1))
        out.flush()
    }

    private fun copyStream(input: java.io.InputStream, output: java.io.OutputStream) {
        try { input.copyTo(output); output.flush() } catch (_: Exception) {}
    }

    private fun stopProxy() {
        running.set(false); isRunning = false
        try { server?.close() } catch (_: Exception) {}
        server = null
    }

    override fun onDestroy() {
        stopProxy(); workers.shutdownNow(); super.onDestroy()
    }
    override fun onBind(intent: Intent?): IBinder? = null
}
''')

manifest = read("AndroidManifest.xml")
manifest = manifest.replace('<uses-permission android:name="android.permission.INTERNET" />',
    '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />')
manifest = manifest.replace('android:icon="@drawable/ic_vpn"', 'android:icon="@drawable/ic_compass"')
if 'android:name=".ProxyService"' not in manifest:
    manifest = manifest.replace('        <!-- VPN Service -->', '''        <service android:name=".ProxyService" android:exported="false" android:foregroundServiceType="specialUse">
            <property android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"
                android:value="Authenticated LAN HTTP proxy over Cloudflare MASQUE" />
        </service>
        <!-- VPN Service -->''')
write("AndroidManifest.xml", manifest)

gradle = ROOT.parents[2] / "app/build.gradle.kts"
build = gradle.read_text(encoding="utf-8").replace("versionCode = 5", "versionCode = 6")
build = build.replace('versionName = "1.1.0"', 'versionName = "1.2.0"')
gradle.write_text(build, encoding="utf-8")

print("Hide Wi-Fi HTTP proxy customization applied.")
