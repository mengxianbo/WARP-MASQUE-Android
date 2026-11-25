package com.abobo.usquevpn

import io.nekohasekai.libbox.Libbox

/** Runtime identity for the unified sing-box + WARP Go library. */
object SingBoxCoreInfo {
    fun version(): String = Libbox.version()
    fun warpVersion(): String = Libbox.warpGetVersion()
}
