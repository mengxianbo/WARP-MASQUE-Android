#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "upstream/usque-android/android/usque-vpn/app/src/main"
def read(p):
    f = ROOT / p
    return f.read_text(encoding="utf-8")
def write(p, s):
    (ROOT / p).write_text(s, encoding="utf-8")

# App name and Chinese UI resources.
write("res/values/strings.xml", '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">JianxianAPP Warp</string>
</resources>
''')

layout = read("res/layout/activity_main.xml")
repls = {
    'android:text="Usque VPN"':'android:text="JianxianAPP Warp"',
    'android:text="Status"':'android:text="连接状态"',
    'android:text="Disconnected"':'android:text="未连接"',
    'android:text="Your IP Address"':'android:text="WARP 分配的 IP 地址"',
    'android:text="Not registered"':'android:text="尚未注册"',
    'android:text="SNI: www.visa.cn"':'android:text="SNI：自动"',
    'android:text="Endpoint: 162.159.198.1"':'android:text="连接节点：默认节点"',
    'android:text="⚙ Settings"':'android:text="⚙ 设置"',
    'android:text="Connect"':'android:text="连接"',
    'android:text="Powered by usque"':'android:text="JianxianAPP Warp · MASQUE 核心由 usque 提供"',
}
for a,b in repls.items(): layout = layout.replace(a,b)
needle = '''    <!-- Footer -->'''
button = '''    <Button
        android:id="@+id/ip_list_button"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:text="管理 IP 节点"
        android:textSize="14sp"
        android:layout_marginTop="4dp"
        android:background="@drawable/button_secondary_background"
        android:textColor="#ffffff" />

    <!-- Footer -->'''
if 'id="@+id/ip_list_button"' not in layout:
    layout = layout.replace(needle, button)
write("res/layout/activity_main.xml", layout)

settings = '''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="24dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="SNI（服务器名称）"
        android:textColor="#666666"
        android:textSize="13sp"
        android:layout_marginBottom="4dp" />
    <EditText
        android:id="@+id/sni_input"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="留空则使用核心默认值"
        android:inputType="textUri"
        android:layout_marginBottom="16dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="当前连接 IP（可在“管理 IP 节点”中保存多个）"
        android:textColor="#666666"
        android:textSize="13sp"
        android:layout_marginBottom="4dp" />
    <EditText
        android:id="@+id/endpoint_input"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="例如：162.159.198.1:443"
        android:inputType="textUri"
        android:layout_marginBottom="8dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="支持 IPv4、IPv6；端口可省略（默认 443）。SNI 应填写服务端要求的域名，不要随意填写无关网站。"
        android:textColor="#888888"
        android:textSize="12sp"
        android:lineSpacingExtra="3dp" />
</LinearLayout>
</ScrollView>
'''
write("res/layout/dialog_settings.xml", settings)

k = read("kotlin/com/abobo/usquevpn/MainActivity.kt")
k = k.replace('private const val KEY_ENDPOINT = "endpoint"', 'private const val KEY_ENDPOINT = "endpoint"\n        private const val KEY_ENDPOINTS = "endpoints"')
k = k.replace('private lateinit var settingsButton: Button', 'private lateinit var settingsButton: Button\n    private lateinit var ipListButton: Button')
k = k.replace('settingsButton = findViewById(R.id.settings_button)', 'settingsButton = findViewById(R.id.settings_button)\n        ipListButton = findViewById(R.id.ip_list_button)')
k = k.replace('settingsButton.setOnClickListener { showSettingsDialog() }', 'settingsButton.setOnClickListener { showSettingsDialog() }\n        ipListButton.setOnClickListener { showEndpointManager() }')
k = k.replace('prefs.getString(KEY_SNI, "www.visa.cn") ?: "www.visa.cn"', 'prefs.getString(KEY_SNI, "") ?: ""')
k = k.replace('prefs.getString(KEY_SNI, Usqueandroid.getSNI())', 'prefs.getString(KEY_SNI, "")')
k = k.replace('prefs.getString(KEY_SNI, Usqueandroid.getSNI()) ?: "www.visa.cn"', 'prefs.getString(KEY_SNI, "") ?: ""')
k = k.replace('saveSettings("www.visa.cn", "")', 'saveSettings("", "")')
k = k.replace('sniText.text = "SNI: $currentSni"', 'sniText.text = if (currentSni.isBlank()) "SNI：自动（核心默认值）" else "SNI：$currentSni"')
k = k.replace('.setTitle("Connection Settings")', '.setTitle("连接设置")')
k = k.replace('.setPositiveButton("Save")', '.setPositiveButton("保存")')
k = k.replace('.setNegativeButton("Cancel", null)', '.setNegativeButton("取消", null)')
k = k.replace('.setNeutralButton("Reset")', '.setNeutralButton("恢复默认")')
k = k.replace('Toast.makeText(this, "Settings saved",', 'Toast.makeText(this, "设置已保存",')
k = k.replace('Toast.makeText(this, "Settings reset to defaults",', 'Toast.makeText(this, "已恢复默认设置",')
k = k.replace('statusText.text = "Connected"', 'statusText.text = "已连接"')
k = k.replace('statusText.text = "Connecting…"', 'statusText.text = "正在连接…"')
k = k.replace('connectButton.text = "Disconnect"', 'connectButton.text = "断开连接"')
k = k.replace('statusText.text = "Disconnected"', 'statusText.text = "未连接"')
k = k.replace('connectButton.text = "Connect"', 'connectButton.text = "连接"')
k = k.replace('ipInfoText.text = "IPv4: $ipv4\\nIPv6: $ipv6"', 'ipInfoText.text = "IPv4：$ipv4\\nIPv6：$ipv6"')
k = k.replace('ipInfoText.text = "Not registered"', 'ipInfoText.text = "尚未注册"')
k = k.replace('endpointText.text = "Endpoint: $displayEndpoint"', 'endpointText.text = "连接节点：$displayEndpoint"')
k = k.replace("settingsButton.isEnabled = false", "settingsButton.isEnabled = false\\n            ipListButton.isEnabled = false")
k = k.replace("settingsButton.isEnabled = true", "settingsButton.isEnabled = true\\n            ipListButton.isEnabled = true")
insert = r'''
    private fun savedEndpoints(): MutableList<String> {
        val raw = prefs.getString(KEY_ENDPOINTS, "") ?: ""
        val values = raw.lines().map { it.trim() }.filter { it.isNotEmpty() }.distinct().toMutableList()
        if (values.isEmpty()) {
            val configPath = "${filesDir.absolutePath}/config.json"
            val fallback = prefs.getString(KEY_ENDPOINT, "")?.trim().orEmpty()
                .ifEmpty { Usqueandroid.getDefaultEndpoint(configPath) }
            if (fallback.isNotEmpty()) values.add(fallback)
        }
        return values
    }

    private fun persistEndpoints(values: List<String>) {
        prefs.edit().putString(KEY_ENDPOINTS, values.joinToString("\\n")).apply()
    }

    private fun showEndpointManager() {
        val endpoints = savedEndpoints()
        val labels = if (endpoints.isEmpty()) arrayOf("暂无 IP 节点") else endpoints.toTypedArray()
        AlertDialog.Builder(this)
            .setTitle("IP 节点列表")
            .setItems(labels) { _, which ->
                if (which in endpoints.indices) {
                    val selected = endpoints[which]
                    prefs.edit().putString(KEY_ENDPOINT, selected).apply()
                    Usqueandroid.setEndpoint(selected)
                    Toast.makeText(this, "已选择节点：$selected", Toast.LENGTH_SHORT).show()
                    updateUI()
                }
            }
            .setPositiveButton("添加 IP") { _, _ -> showAddEndpointDialog() }
            .setNeutralButton("删除最后一个") { _, _ ->
                if (endpoints.isNotEmpty()) {
                    endpoints.removeAt(endpoints.lastIndex)
                    persistEndpoints(endpoints)
                    val selected = endpoints.lastOrNull().orEmpty()
                    prefs.edit().putString(KEY_ENDPOINT, selected).apply()
                    Usqueandroid.setEndpoint(selected)
                    Toast.makeText(this, "已删除最后一个节点", Toast.LENGTH_SHORT).show()
                    updateUI()
                }
            }
            .setNegativeButton("关闭", null)
            .show()
    }

    private fun showAddEndpointDialog() {
        val input = EditText(this).apply {
            hint = "IPv4:443 或 [IPv6]:443"
            setSingleLine(true)
        }
        AlertDialog.Builder(this)
            .setTitle("添加 IP 节点")
            .setMessage("输入 Cloudflare MASQUE 连接端点 IP，可附加端口。")
            .setView(input)
            .setPositiveButton("添加") { _, _ ->
                val value = input.text.toString().trim()
                if (value.isEmpty()) {
                    Toast.makeText(this, "IP 不能为空", Toast.LENGTH_SHORT).show()
                } else {
                    val endpoints = savedEndpoints()
                    if (!endpoints.contains(value)) endpoints.add(value)
                    persistEndpoints(endpoints)
                    prefs.edit().putString(KEY_ENDPOINT, value).apply()
                    Usqueandroid.setEndpoint(value)
                    Toast.makeText(this, "节点已添加并设为当前节点", Toast.LENGTH_SHORT).show()
                    updateUI()
                }
            }
            .setNegativeButton("取消", null)
            .show()
    }
'''
if 'private fun showEndpointManager()' not in k:
    k = k.replace('    private fun startVpn() {', insert + '\n    private fun startVpn() {')
write("kotlin/com/abobo/usquevpn/MainActivity.kt", k)

# Remove the unrelated hard-coded Visa SNI. Empty means use the MASQUE core's own default.
go = ROOT.parents[4] / "usque_android.go"
if go.exists():
    source = go.read_text(encoding="utf-8")
    source = source.replace('customSNI      = "www.visa.cn" // Default SNI for censorship circumvention.', 'customSNI      = "" // Empty uses the MASQUE core default SNI.')
    source = source.replace('customSNI = "www.visa.cn"', 'customSNI = ""')
    go.write_text(source, encoding="utf-8")

# Chinese notification/session labels.
service = read("kotlin/com/abobo/usquevpn/UsqueVpnService.kt")
service = service.replace('"Usque WARP VPN"', '"JianxianAPP Warp"')
service = service.replace('"Connecting…"', '"正在连接…"')
service = service.replace('"Connected"', '"已连接"')
service = service.replace('"Reconnecting…"', '"正在重连…"')
service = service.replace('"Error"', '"连接错误"')
service = service.replace('"Usque VPN"', '"JianxianAPP Warp"')
service = service.replace('"Usque MASQUE VPN status"', '"JianxianAPP Warp 连接状态"')
write("kotlin/com/abobo/usquevpn/UsqueVpnService.kt", service)
print("Applied JianxianAPP Warp branding, Chinese UI, editable SNI default, and multiple endpoint list.")
