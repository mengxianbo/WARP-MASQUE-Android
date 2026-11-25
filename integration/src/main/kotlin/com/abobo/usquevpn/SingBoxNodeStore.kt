package com.abobo.usquevpn

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.net.URI
import java.net.URLDecoder
import java.util.UUID

/** Persists imported proxy profiles and separately managed SOCKS/HTTP outbounds. */
class SingBoxNodeStore(context: Context) {
    data class Node(val id: String, val name: String, val scheme: String, val shareUri: String, val route: String)
    data class OutboundProxy(val id: String, val name: String, val type: String, val host: String, val port: Int, val username: String, val password: String, val tls: Boolean)

    private val prefs = context.getSharedPreferences("singbox_nodes", Context.MODE_PRIVATE)
    private val key = "profiles"
    private val outboundKey = "custom_outbounds"
    private val supported = setOf("vless", "vmess", "trojan", "ss", "shadowsocks", "hysteria2", "hy2", "tuic", "wireguard", "wg", "socks", "socks5", "socks5h", "socks4", "http", "https", "anytls")

    @Synchronized fun all(): List<Node> {
        val a = JSONArray(prefs.getString(key, "[]"))
        return (0 until a.length()).mapNotNull { i ->
            val o = a.optJSONObject(i) ?: return@mapNotNull null
            Node(o.optString("id"), o.optString("name"), o.optString("scheme"), o.optString("uri"), o.optString("route", "warp"))
        }
    }

    @Synchronized fun importOne(raw: String): Node {
        val value = raw.trim()
        require(value.isNotEmpty()) { "节点链接不能为空" }
        require(value.contains("://")) { "节点链接格式无效" }
        val scheme = value.substringBefore(':').lowercase()
        require(scheme in supported) { "暂不支持该协议：$scheme" }
        val uri = runCatching { URI(value) }.getOrNull()
        if (scheme == "vless") {
            require(uri != null) { "VLESS URL 格式无效" }
            val query = parseQuery(uri.rawQuery.orEmpty())
            require(query["type"]?.lowercase() == "ws") { "目前 VLESS 仅支持 WebSocket：请使用 VLESS+WS 或 VLESS+WS+TLS 链接" }
            val security = query["security"]?.lowercase().orEmpty()
            require(security.isEmpty() || security == "none" || security == "tls") { "目前 VLESS WebSocket 仅支持无 TLS 或 TLS，不支持 REALITY 等其他安全类型" }
            require(uri.host != null && uri.port in 1..65535 && uri.userInfo?.isNotBlank() == true) { "VLESS 链接必须包含 UUID、服务器地址和有效端口" }
        } else if (uri == null) {
            require(value.substringAfter("://").isNotBlank()) { "节点链接内容为空" }
        }
        val fragment = value.substringAfter('#', "").takeIf { it.isNotBlank() }
        val name = fragment?.let { runCatching { URLDecoder.decode(it, "UTF-8") }.getOrDefault(it) } ?: scheme.uppercase()
        val n = Node(UUID.randomUUID().toString(), name, scheme, value, "warp")
        saveNodes(all() + n)
        return n
    }

    private fun parseQuery(raw: String): Map<String, String> = raw.split('&').filter { it.isNotBlank() }.associate {
        val parts = it.split('=', limit = 2)
        URLDecoder.decode(parts[0], "UTF-8") to URLDecoder.decode(parts.getOrElse(1) { "" }, "UTF-8")
    }

    @Synchronized fun proxies(): List<OutboundProxy> {
        val a = JSONArray(prefs.getString(outboundKey, "[]"))
        return (0 until a.length()).mapNotNull { i ->
            val o = a.optJSONObject(i) ?: return@mapNotNull null
            OutboundProxy(o.optString("id"), o.optString("name"), o.optString("type"), o.optString("host"), o.optInt("port"), o.optString("username"), o.optString("password"), o.optBoolean("tls"))
        }
    }

    @Synchronized fun addProxy(name: String, type: String, host: String, port: Int, username: String, password: String, tls: Boolean): OutboundProxy {
        require(type == "socks" || type == "http") { "代理类型无效" }
        require(name.isNotBlank()) { "请填写名称" }
        require(host.isNotBlank() && !host.contains("://") && !host.contains('/')) { "服务器地址无效，请只填写域名或 IP" }
        require(port in 1..65535) { "端口必须在 1-65535 之间" }
        require(type != "socks" || !tls) { "SOCKS5 不使用此 HTTPS/TLS 选项" }
        val item = OutboundProxy(UUID.randomUUID().toString(), name.trim(), type, host.trim(), port, username, password, tls)
        saveProxies(proxies() + item)
        return item
    }

    @Synchronized fun removeProxy(id: String) {
        saveProxies(proxies().filterNot { it.id == id })
        saveNodes(all().map { if (it.route == "proxy:$id") it.copy(route = "direct") else it })
    }

    @Synchronized fun setRoute(id: String, route: String) {
        require(route == "warp" || route == "direct" || (route.startsWith("proxy:") && proxies().any { it.id == route.removePrefix("proxy:") })) { "所选出口不存在" }
        saveNodes(all().map { if (it.id == id) it.copy(route = route) else it })
    }

    @Synchronized fun rename(id: String, name: String) {
        require(name.isNotBlank())
        saveNodes(all().map { if (it.id == id) it.copy(name = name.trim()) else it })
    }

    @Synchronized fun remove(id: String) = saveNodes(all().filterNot { it.id == id })

    private fun saveNodes(nodes: List<Node>) {
        val a = JSONArray()
        nodes.forEach { n -> a.put(JSONObject().put("id", n.id).put("name", n.name).put("scheme", n.scheme).put("uri", n.shareUri).put("route", n.route)) }
        prefs.edit().putString(key, a.toString()).apply()
    }

    private fun saveProxies(items: List<OutboundProxy>) {
        val a = JSONArray()
        items.forEach { p ->
            a.put(JSONObject().put("id", p.id).put("name", p.name).put("type", p.type).put("host", p.host).put("port", p.port).put("username", p.username).put("password", p.password).put("tls", p.tls))
        }
        prefs.edit().putString(outboundKey, a.toString()).apply()
    }
}
