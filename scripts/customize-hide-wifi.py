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
   <Button android:id="@+id/proxy_button" android:layout_width="match_parent" android:layout_height="50dp"
    android:text="启动 SOCKS5 代理（端口 6668）" android:textColor="#ffffff"
    android:background="@drawable/button_secondary_background" android:layout_marginTop="12dp"/>
   <TextView android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="SOCKS5（TCP）· 强制用户名和密码认证。目标域名经 Cloudflare MASQUE 远端解析，不在手机本地查询。"
    android:textColor="#9ca3af" android:textSize="11sp" android:layout_marginTop="8dp"/>
   <TextView android:layout_width="match_parent" android:layout_height="wrap_content"
    android:text="WebRTC 提醒：此共享代理不转发 UDP，其他设备需在浏览器禁用 WebRTC，或在该设备启用 VPN。"
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
import android.widget.TextView
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
    private fun ensureProxyCredentials() {
        if (prefs.getString(KEY_PROXY_USER, null) == null || prefs.getString(KEY_PROXY_PASS, null) == null) {
            val alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
            val random = SecureRandom()
            val password = buildString { repeat(20) { append(alphabet[random.nextInt(alphabet.length)]) } }
            prefs.edit().putString(KEY_PROXY_USER, "hidewifi").putString(KEY_PROXY_PASS, password).apply()
        }
    }
    private fun startProxy() {
        val configPath = filesDir.absolutePath + "/config.json"
        if (!Usqueandroid.isRegistered(configPath)) {
            Toast.makeText(this, "请先连接一次 WARP 完成注册，再启动共享代理", Toast.LENGTH_LONG).show()
            return
        }
        ensureProxyCredentials()
        val intent = Intent(this, ProxyService::class.java)
        intent.putExtra(ProxyService.EXTRA_USERNAME, prefs.getString(KEY_PROXY_USER, "hidewifi"))
        intent.putExtra(ProxyService.EXTRA_PASSWORD, prefs.getString(KEY_PROXY_PASS, ""))
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
        ensureProxyCredentials()
        val info = "SOCKS5 " + getWifiIpAddress() + ":" + PROXY_PORT +
            "\n用户名：" + prefs.getString(KEY_PROXY_USER, "hidewifi") +
            "\n密码：" + prefs.getString(KEY_PROXY_PASS, "")
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("Hide Wi-Fi SOCKS5", info))
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
        if (ProxyService.isRunning) {
            ensureProxyCredentials()
            proxyButton.text = "停止 SOCKS5 代理"
            proxyInfoText.text = "SOCKS5 地址：" + getWifiIpAddress() + ":" + PROXY_PORT +
                "\n用户名：" + prefs.getString(KEY_PROXY_USER, "hidewifi") +
                "\n密码：" + prefs.getString(KEY_PROXY_PASS, "") + "\n\n点击复制连接信息"
        } else {
            proxyButton.text = "启动 SOCKS5 代理（端口 6668）"
            proxyInfoText.text = "代理未启动。启动后点击此处可复制连接信息。"
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
import android.widget.Toast
import androidx.core.app.NotificationCompat
import usqueandroid.Usqueandroid

class ProxyService : Service() {
    companion object {
        const val ACTION_STOP = "com.abobo.usquevpn.PROXY_STOP"
        const val EXTRA_USERNAME = "proxy_username"
        const val EXTRA_PASSWORD = "proxy_password"
        private const val CHANNEL_ID = "hide_wifi_proxy"
        private const val NOTIFICATION_ID = 1002
        @Volatile var isRunning = false
            private set
    }
    override fun onCreate() {
        super.onCreate()
        val channel = NotificationChannel(CHANNEL_ID, "Hide Wi-Fi 代理", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
    }
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            Usqueandroid.stopSocksProxy()
            isRunning = false
            stopForeground(true)
            stopSelf()
            return START_NOT_STICKY
        }
        val launch = packageManager.getLaunchIntentForPackage(packageName)
        val pending = if (launch == null) null else PendingIntent.getActivity(this, 0, launch,
            PendingIntent.FLAG_UPDATE_CURRENT or if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0)
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_compass).setContentTitle("Hide Wi-Fi SOCKS5")
            .setContentText("局域网代理监听端口 6668").setOngoing(true)
            .setCategory(NotificationCompat.CATEGORY_SERVICE).setContentIntent(pending).build()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE)
            startForeground(NOTIFICATION_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE)
        else startForeground(NOTIFICATION_ID, notification)
        val user = intent?.getStringExtra(EXTRA_USERNAME) ?: "hidewifi"
        val pass = intent?.getStringExtra(EXTRA_PASSWORD) ?: ""
        val err = Usqueandroid.startSocksProxy(filesDir.absolutePath + "/config.json", "0.0.0.0", 6668, user, pass)
        if (err.isNotEmpty()) {
            isRunning = false
            stopForeground(true)
            stopSelf()
            Toast.makeText(this, "代理启动失败：" + err, Toast.LENGTH_LONG).show()
        } else isRunning = true
        return START_NOT_STICKY
    }
    override fun onDestroy() {
        Usqueandroid.stopSocksProxy()
        isRunning = false
        super.onDestroy()
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
                android:value="Authenticated LAN SOCKS5 proxy over Cloudflare MASQUE" />
        </service>
        <!-- VPN Service -->''')
write("AndroidManifest.xml", manifest)

gradle = ROOT.parents[2] / "app/build.gradle.kts"
build = gradle.read_text(encoding="utf-8").replace("versionCode = 5", "versionCode = 6")
build = build.replace('versionName = "1.1.0"', 'versionName = "1.2.0"')
gradle.write_text(build, encoding="utf-8")

l4 = REPO / "upstream/usque-android/api/l4proxy.go"
l4src = l4.read_text(encoding="utf-8")
if "func (p *L4Proxy) Close()" not in l4src:
    l4src += """
// Close releases the cached HTTP/3 connection used by this L4 proxy.
func (p *L4Proxy) Close() error {
    if p == nil { return nil }
    p.connMu.Lock()
    client := p.client
    p.client = nil
    p.connMu.Unlock()
    if client != nil { closeL4HTTP3(client.udpConn, client.quicConn) }
    return nil
}
"""
    l4.write_text(l4src, encoding="utf-8")

go = REPO / "upstream/usque-android/android/usque_android.go"
src = go.read_text(encoding="utf-8")
if '"crypto/subtle"' not in src:
    src = src.replace('"context"\n', '"context"\n\t"crypto/subtle"\n')
if '"encoding/binary"' not in src:
    src = src.replace('"fmt"\n', '"fmt"\n\t"encoding/binary"\n')
if '"github.com/quic-go/quic-go"' not in src:
    src = src.replace('"github.com/Diniboy1123/usque/internal"\n', '"github.com/Diniboy1123/usque/internal"\n\tquic "github.com/quic-go/quic-go"\n')

proxy_code = r"""
type lanSocksProxyState struct {
    mu sync.Mutex
    listener net.Listener
    proxy *api.L4Proxy
    cancel context.CancelFunc
    clients map[net.Conn]struct{}
}
var lanProxy = &lanSocksProxyState{clients: make(map[net.Conn]struct{})}

// StartSocksProxy starts a password-protected TCP-only SOCKS5 proxy.
// Domain names are sent through MASQUE CONNECT for remote DNS resolution.
func StartSocksProxy(configPath string, bindAddress string, port int, username string, password string) string {
    lanProxy.mu.Lock()
    defer lanProxy.mu.Unlock()
    if lanProxy.listener != nil { return "SOCKS5 proxy is already running" }
    if username == "" || password == "" { return "SOCKS5 username and password are required" }
    if port < 1 || port > 65535 { return "invalid SOCKS5 port" }
    if err := config.LoadConfig(configPath); err != nil { return fmt.Sprintf("load config: %v", err) }
    privKey, err := config.AppConfig.GetEcPrivateKey()
    if err != nil { return fmt.Sprintf("private key: %v", err) }
    peerPubKey, err := config.AppConfig.GetEcEndpointPublicKey()
    if err != nil { return fmt.Sprintf("peer public key: %v", err) }
    cert, err := internal.GenerateCert(privKey, &privKey.PublicKey)
    if err != nil { return fmt.Sprintf("client certificate: %v", err) }
    tlsConfig, err := api.PrepareTlsConfig(privKey, peerPubKey, cert, internal.L4ConnectSNI, false)
    if err != nil { return fmt.Sprintf("TLS config: %v", err) }
    endpointAddr, err := config.SelectEndpointFromConfig(false, false, 443)
    if err != nil { return fmt.Sprintf("MASQUE endpoint: %v", err) }
    endpoint, ok := endpointAddr.(*net.UDPAddr)
    if !ok || endpoint == nil { return "invalid MASQUE UDP endpoint" }
    l4, err := api.NewL4Proxy(api.L4ProxyConfig{
        TLSConfig: tlsConfig,
        QUICConfig: &quic.Config{
            EnableDatagrams: false, KeepAlivePeriod: 30*time.Second,
            InitialConnectionReceiveWindow: 10_000_000, MaxConnectionReceiveWindow: 10_000_000,
            InitialStreamReceiveWindow: 1_000_000, MaxStreamReceiveWindow: 1_000_000,
            MaxIncomingStreams: 100, MaxIncomingUniStreams: 100,
        },
        Endpoint: endpoint, ResolveLocally: false,
        ConnectTimeout: 15*time.Second, ConnectRetryCount: 2,
    })
    if err != nil { return fmt.Sprintf("create MASQUE proxy: %v", err) }
    listener, err := net.Listen("tcp", net.JoinHostPort(bindAddress, strconv.Itoa(port)))
    if err != nil { _ = l4.Close(); return fmt.Sprintf("listen: %v", err) }
    ctx, cancel := context.WithCancel(context.Background())
    lanProxy.listener, lanProxy.proxy, lanProxy.cancel = listener, l4, cancel
    lanProxy.clients = make(map[net.Conn]struct{})
    go acceptLanSocks(ctx, listener, l4, username, password)
    return ""
}

// StopSocksProxy closes the listener, client sockets, and shared MASQUE connection.
func StopSocksProxy() {
    lanProxy.mu.Lock()
    listener, proxy, cancel := lanProxy.listener, lanProxy.proxy, lanProxy.cancel
    clients := make([]net.Conn, 0, len(lanProxy.clients))
    for c := range lanProxy.clients { clients = append(clients, c) }
    lanProxy.listener, lanProxy.proxy, lanProxy.cancel = nil, nil, nil
    lanProxy.clients = make(map[net.Conn]struct{})
    lanProxy.mu.Unlock()
    if cancel != nil { cancel() }
    if listener != nil { _ = listener.Close() }
    for _, c := range clients { _ = c.Close() }
    if proxy != nil { _ = proxy.Close() }
}

// IsSocksProxyRunning reports whether the LAN SOCKS5 listener is active.
func IsSocksProxyRunning() bool {
    lanProxy.mu.Lock()
    defer lanProxy.mu.Unlock()
    return lanProxy.listener != nil
}

func acceptLanSocks(ctx context.Context, listener net.Listener, proxy *api.L4Proxy, username, password string) {
    for {
        conn, err := listener.Accept()
        if err != nil { return }
        lanProxy.mu.Lock()
        if lanProxy.listener != listener {
            lanProxy.mu.Unlock()
            _ = conn.Close()
            return
        }
        lanProxy.clients[conn] = struct{}{}
        lanProxy.mu.Unlock()
        go func(c net.Conn) {
            defer func() {
                _ = c.Close()
                lanProxy.mu.Lock()
                delete(lanProxy.clients, c)
                lanProxy.mu.Unlock()
            }()
            serveLanSocks(ctx, c, proxy, username, password)
        }(conn)
    }
}

func serveLanSocks(ctx context.Context, client net.Conn, proxy *api.L4Proxy, username, password string) {
    _ = client.SetDeadline(time.Now().Add(20*time.Second))
    var head [2]byte
    if _, err := io.ReadFull(client, head[:]); err != nil || head[0] != 5 { return }
    methods := make([]byte, int(head[1]))
    if _, err := io.ReadFull(client, methods); err != nil { return }
    hasAuth := false
    for _, method := range methods { if method == 2 { hasAuth = true } }
    if !hasAuth { _, _ = client.Write([]byte{5, 0xff}); return }
    if _, err := client.Write([]byte{5, 2}); err != nil { return }

    var authHead [2]byte
    if _, err := io.ReadFull(client, authHead[:]); err != nil || authHead[0] != 1 { return }
    userBytes := make([]byte, int(authHead[1]))
    if _, err := io.ReadFull(client, userBytes); err != nil { return }
    var passLen [1]byte
    if _, err := io.ReadFull(client, passLen[:]); err != nil { return }
    passBytes := make([]byte, int(passLen[0]))
    if _, err := io.ReadFull(client, passBytes); err != nil { return }
    if subtle.ConstantTimeCompare(userBytes, []byte(username)) != 1 || subtle.ConstantTimeCompare(passBytes, []byte(password)) != 1 {
        _, _ = client.Write([]byte{1, 1})
        return
    }
    if _, err := client.Write([]byte{1, 0}); err != nil { return }

    var req [4]byte
    if _, err := io.ReadFull(client, req[:]); err != nil || req[0] != 5 { return }
    if req[1] != 1 { _, _ = client.Write([]byte{5, 7, 0, 1, 0, 0, 0, 0, 0, 0}); return }
    var host string
    switch req[3] {
    case 1:
        b := make([]byte, 4); if _, err := io.ReadFull(client, b); err != nil { return }; host = net.IP(b).String()
    case 3:
        var n [1]byte; if _, err := io.ReadFull(client, n[:]); err != nil { return }
        b := make([]byte, int(n[0])); if _, err := io.ReadFull(client, b); err != nil { return }; host = string(b)
    case 4:
        b := make([]byte, 16); if _, err := io.ReadFull(client, b); err != nil { return }; host = net.IP(b).String()
    default:
        _, _ = client.Write([]byte{5, 8, 0, 1, 0, 0, 0, 0, 0, 0}); return
    }
    var portBytes [2]byte
    if _, err := io.ReadFull(client, portBytes[:]); err != nil { return }
    port := int(binary.BigEndian.Uint16(portBytes[:]))
    if host == "" || port == 0 { _, _ = client.Write([]byte{5, 1, 0, 1, 0, 0, 0, 0, 0, 0}); return }
    _ = client.SetDeadline(time.Time{})
    upstream, err := proxy.DialContext(ctx, net.JoinHostPort(host, strconv.Itoa(port)))
    if err != nil {
        _, _ = client.Write([]byte{5, 5, 0, 1, 0, 0, 0, 0, 0, 0})
        return
    }
    if _, err := client.Write([]byte{5, 0, 0, 1, 0, 0, 0, 0, 0, 0}); err != nil { _ = upstream.Close(); return }
    api.RelayTCP(client, upstream)
}

"""
if "func StartSocksProxy(" not in src:
    src = src.replace("// GetVersion returns the Android wrapper version.", proxy_code + "// GetVersion returns the Android wrapper version.")
src = src.replace('return "1.1.0-android"', 'return "1.2.0-android"')
go.write_text(src, encoding="utf-8")
print("Hide Wi-Fi 1.2.0 customization applied.")
