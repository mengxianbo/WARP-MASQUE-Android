package com.abobo.usquevpn

import android.app.Activity
import android.app.AlertDialog
import android.os.Bundle
import android.text.InputType
import android.view.ViewGroup
import android.widget.*

class NodeProfilesActivity : Activity() {
    private lateinit var store: SingBoxNodeStore
    private lateinit var list: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        store = SingBoxNodeStore(this)
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(24, 24, 24, 24) }
        root.addView(TextView(this).apply { text = "sing-box 节点管理"; textSize = 22f })
        root.addView(TextView(this).apply {
            text = "内核版本：${runCatching { SingBoxCoreInfo.version() }.getOrDefault("读取失败")}"
            textSize = 13f
        })
        root.addView(Button(this).apply { text = "导入单个节点 URL"; setOnClickListener { importDialog() } })
        root.addView(TextView(this).apply {
            text = "VLESS 支持 WS 和 WS+TLS；同时保留 VMess、Trojan、SS、Hysteria2、TUIC、WireGuard、AnyTLS 等导入入口。下方可添加 SOCKS5、HTTP 或 HTTPS 自定义出口。注意：当前页面保存管理配置，尚未接入 sing-box 运行时，不能据此认为实际流量已按所选出口转发。"
            textSize = 12f
        })
        root.addView(TextView(this).apply { text = "已导入节点"; textSize = 18f })
        list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        root.addView(ScrollView(this).apply { addView(list) }, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        root.addView(TextView(this).apply { text = "自定义出站"; textSize = 18f })
        val actions = LinearLayout(this)
        actions.addView(Button(this).apply { text = "添加 SOCKS5"; setOnClickListener { proxyDialog("socks") } })
        actions.addView(Button(this).apply { text = "添加 HTTP/HTTPS"; setOnClickListener { proxyDialog("http") } })
        root.addView(actions)
        setContentView(root)
        refresh()
    }

    private fun importDialog() {
        val input = EditText(this).apply { hint = "粘贴单个 vless://、vmess://、ss:// 等链接"; minLines = 2; maxLines = 5 }
        AlertDialog.Builder(this).setTitle("导入单节点").setView(input)
            .setPositiveButton("导入") { _, _ ->
                try {
                    val n = store.importOne(input.text.toString())
                    Toast.makeText(this, "已保存：${n.name}", Toast.LENGTH_SHORT).show()
                    refresh()
                } catch (e: Exception) { Toast.makeText(this, e.message ?: "导入失败", Toast.LENGTH_LONG).show() }
            }.setNegativeButton("取消", null).show()
    }

    private fun proxyDialog(type: String) {
        val fields = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(24, 8, 24, 0) }
        fun field(hintText: String, kind: Int = InputType.TYPE_CLASS_TEXT): EditText =
            EditText(this).apply { hint = hintText; inputType = kind; fields.addView(this) }
        val name = field("名称，例如：我的代理出口")
        val host = field("服务器域名或 IP")
        val port = field("端口", InputType.TYPE_CLASS_NUMBER)
        val username = field("用户名（可选）")
        val password = field("密码（可选）", InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD)
        val tls = CheckBox(this).apply {
            text = "HTTPS / TLS"
            visibility = if (type == "http") android.view.View.VISIBLE else android.view.View.GONE
            fields.addView(this)
        }
        AlertDialog.Builder(this).setTitle(if (type == "socks") "添加 SOCKS5 出站" else "添加 HTTP/HTTPS 出站")
            .setView(ScrollView(this).apply { addView(fields) })
            .setPositiveButton("保存") { _, _ ->
                try {
                    store.addProxy(name.text.toString().ifBlank { if (type == "socks") "SOCKS5" else "HTTP" },
                        type, host.text.toString(), port.text.toString().toInt(), username.text.toString(), password.text.toString(), tls.isChecked)
                    refresh()
                    Toast.makeText(this, "出站已保存", Toast.LENGTH_SHORT).show()
                } catch (e: Exception) { Toast.makeText(this, e.message ?: "保存失败", Toast.LENGTH_LONG).show() }
            }.setNegativeButton("取消", null).show()
    }

    private fun routeLabel(route: String): String {
        if (route == "warp") return "WARP"
        if (route == "direct") return "DIRECT"
        val p = store.proxies().firstOrNull { it.id == route.removePrefix("proxy:") }
        return p?.let { "${it.name} (${if (it.type == "socks") "SOCKS5" else if (it.tls) "HTTPS" else "HTTP"})" } ?: "DIRECT"
    }

    private fun chooseRoute(node: SingBoxNodeStore.Node) {
        val proxies = store.proxies()
        val labels = listOf("WARP", "DIRECT") + proxies.map { "${it.name} — ${if (it.type == "socks") "SOCKS5" else if (it.tls) "HTTPS" else "HTTP"}" }
        val values = listOf("warp", "direct") + proxies.map { "proxy:${it.id}" }
        val selected = values.indexOf(node.route).coerceAtLeast(0)
        AlertDialog.Builder(this).setTitle("选择 ${node.name} 的出口")
            .setSingleChoiceItems(labels.toTypedArray(), selected) { dialog, which ->
                try {
                    store.setRoute(node.id, values[which])
                    dialog.dismiss()
                    refresh()
                } catch (e: Exception) { Toast.makeText(this, e.message ?: "设置失败", Toast.LENGTH_LONG).show() }
            }.setNegativeButton("取消", null).show()
    }

    private fun refresh() {
        list.removeAllViews()
        val nodes = store.all()
        if (nodes.isEmpty()) list.addView(TextView(this).apply { text = "还没有导入节点" })
        nodes.forEach { n ->
            val row = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(0, 12, 0, 12) }
            row.addView(TextView(this).apply { text = "${n.name} [${n.scheme.uppercase()}]"; textSize = 16f })
            row.addView(TextView(this).apply { text = "出口选择：${routeLabel(n.route)}"; textSize = 13f })
            val buttons = LinearLayout(this)
            buttons.addView(Button(this).apply { text = "选择出口"; setOnClickListener { chooseRoute(n) } })
            buttons.addView(Button(this).apply { text = "删除节点"; setOnClickListener { store.remove(n.id); refresh() } })
            row.addView(buttons)
            list.addView(row)
        }
        store.proxies().forEach { p ->
            val row = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(0, 8, 0, 8) }
            row.addView(TextView(this).apply {
                text = "${p.name} [${if (p.type == "socks") "SOCKS5" else if (p.tls) "HTTPS" else "HTTP"}]  ${p.host}:${p.port}"
                textSize = 14f
            })
            row.addView(Button(this).apply { text = "删除出站"; setOnClickListener { store.removeProxy(p.id); refresh() } })
            list.addView(row)
        }
    }
}
