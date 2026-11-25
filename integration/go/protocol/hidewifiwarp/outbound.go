package hidewifiwarp

import (
	"context"
	"fmt"
	"net"

	"github.com/sagernet/sing-box/adapter"
	"github.com/sagernet/sing-box/adapter/outbound"
	"github.com/sagernet/sing-box/log"
	"github.com/sagernet/sing-box/option"
	E "github.com/sagernet/sing/common/exceptions"
	M "github.com/sagernet/sing/common/metadata"
	N "github.com/sagernet/sing/common/network"
	"github.com/sagernet/sing/service"

	"github.com/Diniboy1123/usque/api"
)
const outboundType = "warp"

var (
	_ adapter.Outbound              = (*Outbound)(nil)
	_ adapter.Lifecycle             = (*Outbound)(nil)
	_ adapter.InterfaceUpdateListener = (*Outbound)(nil)
)

// Outbound is the TCP MASQUE dialer used as a sing-box detour. It deliberately
// does not own an Android VpnService or TUN descriptor. VLESS uses this dialer
// only to carry its connection to the VLESS server; VLESS UDP payloads can
// still be transported inside the VLESS TCP stream.
type Outbound struct {
	outbound.Adapter
	logger log.ContextLogger
	proxy  *api.L4Proxy
}

func RegisterOutbound(registry *outbound.Registry) {
	outbound.Register[option.WarpOutboundOptions](registry, outboundType, NewOutbound)
}

func NewOutbound(
	ctx context.Context,
	_ adapter.Router,
	logger log.ContextLogger,
	tag string,
	options option.WarpOutboundOptions,
) (adapter.Outbound, error) {
	if options.ConfigPath == "" {
		return nil, E.New("warp outbound: config_path is required")
	}
	networkManager := service.FromContext[adapter.NetworkManager](ctx)
	if networkManager == nil {
		return nil, E.New("warp outbound: sing-box network manager is unavailable")
	}
	protectSocket := networkManager.ProtectFunc()
	if protectSocket == nil {
		return nil, E.New("warp outbound: Android socket protection is unavailable; refusing to risk a TUN loop")
	}
	proxy, err := api.NewL4ProxyFromConfig(
		options.ConfigPath,
		options.SNI,
		func(listenCtx context.Context, remote *net.UDPAddr) (*net.UDPConn, error) {
			network := "udp4"
			local := &net.UDPAddr{IP: net.IPv4zero}
			if remote.IP.To4() == nil {
				network = "udp6"
				local = &net.UDPAddr{IP: net.IPv6unspecified}
			}
			var listenConfig net.ListenConfig
			listenConfig.Control = protectSocket
			packetConn, listenErr := listenConfig.ListenPacket(listenCtx, network, local.String())
			if listenErr != nil {
				return nil, listenErr
			}
			udpConn, ok := packetConn.(*net.UDPConn)
			if !ok {
				_ = packetConn.Close()
				return nil, E.New("warp outbound: protected listener is not UDP")
			}
			return udpConn, nil
		},
	)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: create MASQUE dialer")
	}

	return &Outbound{
		Adapter: outbound.NewAdapter(outboundType, tag, []string{N.NetworkTCP}, nil),
		logger:  logger,
		proxy:   proxy,
	}, nil
}

func (o *Outbound) Start(stage adapter.StartStage, scope *adapter.Scope) error {
	if stage == adapter.StartStateInitialize {
		scope.Add(o.proxy.Close)
	}
	return nil
}

func (o *Outbound) InterfaceUpdated(context.Context) {
	if err := o.proxy.Close(); err != nil {
		o.logger.Warn("close WARP MASQUE connection after network change: ", err)
	}
}

func (o *Outbound) DialContext(ctx context.Context, network string, destination M.Socksaddr) (net.Conn, error) {
	if N.NetworkName(network) != N.NetworkTCP {
		return nil, E.New("warp outbound currently supports TCP streams only")
	}
	o.logger.InfoContext(ctx, "WARP MASQUE CONNECT to ", destination)
	conn, err := o.proxy.DialContext(ctx, destination.String())
	if err != nil {
		return nil, E.Cause(err, fmt.Sprintf("WARP MASQUE CONNECT %s", destination))
	}
	return conn, nil
}

func (o *Outbound) ListenPacket(context.Context, M.Socksaddr) (net.PacketConn, error) {
	return nil, E.New("warp outbound currently supports TCP streams only; UDP standalone mode is not enabled")
}
