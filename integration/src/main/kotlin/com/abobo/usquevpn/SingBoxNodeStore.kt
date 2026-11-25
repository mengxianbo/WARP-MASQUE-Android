package com.abobo.usquevpn

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.net.URI
import java.util.UUID

/** Stores individually imported share links and the user's desired route mode. */
class SingBoxNodeStore(context: Context) {
    data class Node(val id: String, val name: String, val scheme: String, val shareUri: String, val route: String)
    private val prefs = context.getSharedPreferences("singbox_nodes", Context.MODE_PRIVATE)
    private val key = "profiles"
    private val supported = setOf("vless","vmess","trojan","ss","shadowsocks","hysteria2","hy2","tuic","wireguard","wg","socks","socks5","socks5h","socks4","http","https","anytls")

    @Synchronized fun all(): List<Node> {
        val a = JSONArray(prefs.getString(key, "[]"))
        return (0 until a.length()).mapNotNull { i ->
            val o = a.optJSONObject(i) ?: return@mapNotNull null
            Node(o.optString("id"), o.optString("name"), o.optString("scheme"), o.optString("uri"), o.optString("route","warp"))
        }
    }
    @Synchronized fun importOne(raw: String): Node {
        val value = raw.trim()
        require(value.isNotEmpty()) { "节点链接不能为空" }
        require(value.contains("://")) { "节点链接格式无效" }
        val scheme = value.substringBefore(':').lowercase()
        require(scheme in supported) { "暂不支持该协议：$scheme" }
        try { URI(value) } catch (_: Exception) {
            require(value.substringAfter("://").isNotBlank()) { "节点链接内容为空" }
        }
        val fragment = value.substringAfter('#',"").takeIf { it.isNotBlank() }
        val name = fragment?.let { runCatching { java.net.URLDecoder.decode(it,"UTF-8") }.getOrDefault(it) } ?: scheme.uppercase()
        val n = Node(UUID.randomUUID().toString(), name, scheme, value, "warp")
        save(all() + n)
        return n
    }
    @Synchronized fun setRoute(id: String, route: String) {
        require(route == "warp" || route == "direct")
        save(all().map { if (it.id == id) it.copy(route=route) else it })
    }
    @Synchronized fun rename(id: String, name: String) {
        require(name.isNotBlank())
        save(all().map { if (it.id == id) it.copy(name=name.trim()) else it })
    }
    @Synchronized fun remove(id: String) = save(all().filterNot { it.id == id })
    private fun save(nodes: List<Node>) {
        val a = JSONArray()
        nodes.forEach { n -> a.put(JSONObject().put("id",n.id).put("name",n.name).put("scheme",n.scheme).put("uri",n.shareUri).put("route",n.route)) }
        prefs.edit().putString(key,a.toString()).apply()
    }
}
