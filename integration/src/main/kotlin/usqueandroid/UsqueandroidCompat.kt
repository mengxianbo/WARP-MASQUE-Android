package usqueandroid

import io.nekohasekai.libbox.HideWifiWarpPacketFlow
import io.nekohasekai.libbox.HideWifiWarpStateCallback
import io.nekohasekai.libbox.Libbox

/** Compatibility facade: existing WARP Android UI now calls the unified libbox AAR. */
interface PacketFlow {
    fun writePacket(data: ByteArray?)
}

interface VpnStateCallback {
    fun onConnected()
    fun onDisconnected(reason: String?)
    fun onError(message: String?)
}

object Usqueandroid {
    fun register(configPath: String, deviceName: String): String =
        Libbox.warpRegister(configPath, deviceName)

    fun isRegistered(configPath: String): Boolean =
        Libbox.warpIsRegistered(configPath)

    fun getAssignedIPv4(configPath: String): String =
        Libbox.warpGetAssignedIPv4(configPath)

    fun getAssignedIPv6(configPath: String): String =
        Libbox.warpGetAssignedIPv6(configPath)

    fun getDefaultEndpoint(configPath: String): String =
        Libbox.warpGetDefaultEndpoint(configPath)

    fun startTunnel(
        configPath: String,
        tunFd: Long,
        mtu: Int,
        packetFlow: PacketFlow,
        callback: VpnStateCallback
    ): String = Libbox.warpStartTunnel(
        configPath,
        tunFd,
        mtu,
        object : HideWifiWarpPacketFlow {
            override fun writePacket(data: ByteArray?) {
                packetFlow.writePacket(data)
            }
        },
        object : HideWifiWarpStateCallback {
            override fun onConnected() = callback.onConnected()
            override fun onDisconnected(reason: String?) = callback.onDisconnected(reason)
            override fun onError(message: String?) = callback.onError(message)
        }
    )

    fun startTunnelWithFd(configPath: String, tunFd: Long, callback: VpnStateCallback): String =
        Libbox.warpStartTunnelWithFd(
            configPath,
            tunFd,
            object : HideWifiWarpStateCallback {
                override fun onConnected() = callback.onConnected()
                override fun onDisconnected(reason: String?) = callback.onDisconnected(reason)
                override fun onError(message: String?) = callback.onError(message)
            }
        )

    fun stopTunnel() = Libbox.warpStopTunnel()
    fun isRunning(): Boolean = Libbox.warpIsRunning()
    fun isConnected(): Boolean = Libbox.warpIsConnected()
    fun getVersion(): String = Libbox.warpGetVersion()
    fun setSNI(sni: String) = Libbox.warpSetSNI(sni)
    fun getSNI(): String = Libbox.warpGetSNI()
    fun setEndpoint(endpoint: String) = Libbox.warpSetEndpoint(endpoint)
    fun getEndpoint(): String = Libbox.warpGetEndpoint()
    fun resetConnectionOptions() = Libbox.warpResetConnectionOptions()
    fun testEndpoint(configPath: String, endpoint: String, timeoutMs: Long): String =
        Libbox.warpTestEndpoint(configPath, endpoint, timeoutMs)
}
