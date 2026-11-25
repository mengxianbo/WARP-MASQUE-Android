package hidewifiwarp

import (
	"context"
	"crypto/ecdsa"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"net"
	"os"
	"time"

	"github.com/Diniboy1123/usque/api"
	"github.com/Diniboy1123/usque/config"
	"github.com/Diniboy1123/usque/internal"
	"github.com/sagernet/sing-box/adapter"
	"github.com/sagernet/sing-box/adapter/outbound"
	"github.com/sagernet/sing-box/log"
	"github.com/sagernet/sing-box/option"
	E "github.com/sagernet/sing/common/exceptions"
	M "github.com/sagernet/sing/common/metadata"
	N "github.com/sagernet/sing/common/network"
	"github.com/sagernet/sing/service"
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
	rawConfig, err := os.ReadFile(options.ConfigPath)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: read config")
	}
	var warpConfig config.Config
	if err = jsonUnmarshalConfig(rawConfig, &warpConfig); err != nil {
		return nil, E.Cause(err, "warp outbound: decode config")
	}

	privateKeyBytes, err := base64.StdEncoding.DecodeString(warpConfig.PrivateKey)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: decode private key")
	}
	privateKey, err := x509.ParseECPrivateKey(privateKeyBytes)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: parse private key")
	}
	peerPublicKeyBlock, _ := pem.Decode([]byte(warpConfig.EndpointPubKey))
	if peerPublicKeyBlock == nil {
		return nil, E.New("warp outbound: decode endpoint public key PEM")
	}
	parsedPeerKey, err := x509.ParsePKIXPublicKey(peerPublicKeyBlock.Bytes)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: parse endpoint public key")
	}
	peerPublicKey, ok := parsedPeerKey.(*ecdsa.PublicKey)
	if !ok {
		return nil, E.New("warp outbound: endpoint public key is not ECDSA")
	}
	certificate, err := internal.GenerateCert(privateKey, &privateKey.PublicKey)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: generate client certificate")
	}

	sni := options.SNI
	if sni == "" {
		sni = internal.ConnectSNI
	}
	tlsConfig, err := api.PrepareTlsConfig(privateKey, peerPublicKey, certificate, sni, options.Insecure)
	if err != nil {
		return nil, E.Cause(err, "warp outbound: prepare MASQUE TLS")
	}

	var endpointIP net.IP
	if warpConfig.EndpointV4 != "" {
		endpointIP = net.ParseIP(warpConfig.EndpointV4)
	}
	if endpointIP == nil && warpConfig.EndpointV6 != "" {
		endpointIP = net.ParseIP(warpConfig.EndpointV6)
	}
	if endpointIP == nil {
		return nil, E.New("warp outbound: config has no valid MASQUE endpoint IP")
	}
	endpoint := &net.UDPAddr{IP: endpointIP, Port: 443}

	networkManager := service.FromContext[adapter.NetworkManager](ctx)
	if networkManager == nil {
		return nil, E.New("warp outbound: sing-box network manager is unavailable")
	}
	protectSocket := networkManager.ProtectFunc()
	proxy, err := api.NewL4Proxy(api.L4ProxyConfig{
		TLSConfig: tlsConfig,
		Endpoint:  endpoint,
		ListenUDP: func(listenCtx context.Context, remote *net.UDPAddr) (*net.UDPConn, error) {
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
		ConnectTimeout:    15 * time.Second,
		ConnectRetryCount: 2,
	})
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
