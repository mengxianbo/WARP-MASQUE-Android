package com.abobo.usquevpn

import android.app.Activity
import android.app.AlertDialog
import android.os.Bundle
import android.view.ViewGroup
import android.widget.*

class NodeProfilesActivity : Activity() {
    private lateinit var store: SingBoxNodeStore
    private lateinit var list: LinearLayout
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        store = SingBoxNodeStore(this)
        val root = LinearLayout(this).apply { orientation=LinearLayout.VERTICAL; setPadding(24,24,24,24) }
        root.addView(TextView(this).apply { text="sing-box 节点管理"; textSize=22f })
        root.addView(TextView(this).apply {
            text="内核版本：${runCatching { SingBoxCoreInfo.version() }.getOrDefault("读取失败")}"
            textSize=13f
        })
        root.addView(Button(this).apply { text="导入单个节点 URL"; setOnClickListener { importDialog() } })
        root.addView(TextView(this).apply {
            text="支持 VLESS / VMess / Trojan / SS / Hysteria2 / TUIC / WireGuard / AnyTLS / SOCKS / HTTP(S)"
            textSize=12f
        })
        list=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL }
        root.addView(ScrollView(this).apply { addView(list) }, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,0,1f))
        setContentView(root); refresh()
    }
    private fun importDialog() {
        val input=EditText(this).apply { hint="粘贴单个 vless://、vmess://、ss:// 等链接"; minLines=2; maxLines=5 }
        AlertDialog.Builder(this).setTitle("导入单节点").setView(input)
            .setPositiveButton("导入") { _,_ ->
                try { val n=store.importOne(input.text.toString()); Toast.makeText(this,"已保存：${n.name}",Toast.LENGTH_SHORT).show(); refresh() }
                catch(e:Exception) { Toast.makeText(this,e.message ?: "导入失败",Toast.LENGTH_LONG).show() }
            }.setNegativeButton("取消",null).show()
    }
    private fun refresh() {
        list.removeAllViews()
        val nodes=store.all()
        if(nodes.isEmpty()) list.addView(TextView(this).apply { text="还没有导入节点" })
        nodes.forEach { n ->
            val row=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL; setPadding(0,12,0,12) }
            row.addView(TextView(this).apply { text="${n.name} [${n.scheme}]"; textSize=16f })
            row.addView(TextView(this).apply { text="出站偏好：${if(n.route=="warp") "WARP" else "直接"}"; textSize=13f })
            val buttons=LinearLayout(this)
            buttons.addView(Button(this).apply { text="切换出站偏好"; setOnClickListener { store.setRoute(n.id,if(n.route=="warp") "direct" else "warp"); refresh() } })
            buttons.addView(Button(this).apply { text="删除"; setOnClickListener { store.remove(n.id); refresh() } })
            row.addView(buttons); list.addView(row)
        }
    }
}
