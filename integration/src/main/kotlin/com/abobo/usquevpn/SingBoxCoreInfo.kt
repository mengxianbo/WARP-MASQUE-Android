package com.abobo.usquevpn

/** Compile-time/runtime bridge for the official sing-box libbox Android AAR. */
object SingBoxCoreInfo {
    fun version(): String = libbox.Libbox.version()
}
