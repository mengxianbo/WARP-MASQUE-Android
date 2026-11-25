package api

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

	"github.com/Diniboy1123/usque/config"
	"github.com/Diniboy1123/usque/internal"
)

// NewL4ProxyFromConfig creates the pinned Cloudflare MASQUE TCP dialer from a
// private usque account config. listenUDP must create the QUIC underlay socket
// with the host VPN's protect/bypass callback applied.
func NewL4ProxyFromConfig(
	configPath string,
	sni string,
	listenUDP func(context.Context, *net.UDPAddr) (*net.UDPConn, error),
) (*L4Proxy, error) {
	if configPath == "" {
		return nil, fmt.Errorf("missing WARP config path")
	}
	rawConfig, err := os.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("read WARP config: %w", err)
	}
	var warpConfig config.Config
	if err = json.Unmarshal(rawConfig, &warpConfig); err != nil {
		return nil, fmt.Errorf("decode WARP config: %w", err)
	}

	privateKeyBytes, err := base64.StdEncoding.DecodeString(warpConfig.PrivateKey)
	if err != nil {
		return nil, fmt.Errorf("decode WARP private key: %w", err)
	}
	privateKey, err := x509.ParseECPrivateKey(privateKeyBytes)
	if err != nil {
		return nil, fmt.Errorf("parse WARP private key: %w", err)
	}
	peerKeyBlock, _ := pem.Decode([]byte(warpConfig.EndpointPubKey))
	if peerKeyBlock == nil {
		return nil, fmt.Errorf("decode WARP endpoint public key PEM")
	}
	parsedPeerKey, err := x509.ParsePKIXPublicKey(peerKeyBlock.Bytes)
	if err != nil {
		return nil, fmt.Errorf("parse WARP endpoint public key: %w", err)
	}
	peerPublicKey, ok := parsedPeerKey.(*ecdsa.PublicKey)
	if !ok {
		return nil, fmt.Errorf("WARP endpoint public key is not ECDSA")
	}
	certificate, err := internal.GenerateCert(privateKey, &privateKey.PublicKey)
	if err != nil {
		return nil, fmt.Errorf("generate WARP client certificate: %w", err)
	}

	if sni == "" {
		sni = internal.ConnectSNI
	}
	tlsConfig, err := PrepareTlsConfig(privateKey, peerPublicKey, certificate, sni, false)
	if err != nil {
		return nil, fmt.Errorf("prepare pinned WARP MASQUE TLS: %w", err)
	}

	var endpointIP net.IP
	if warpConfig.EndpointV4 != "" {
		endpointIP = net.ParseIP(warpConfig.EndpointV4)
	}
	if endpointIP == nil && warpConfig.EndpointV6 != "" {
		endpointIP = net.ParseIP(warpConfig.EndpointV6)
	}
	if endpointIP == nil {
		return nil, fmt.Errorf("WARP config has no valid MASQUE endpoint IP")
	}

	return NewL4Proxy(L4ProxyConfig{
		TLSConfig:         tlsConfig,
		Endpoint:          &net.UDPAddr{IP: endpointIP, Port: 443},
		ListenUDP:         listenUDP,
		ConnectTimeout:    15 * time.Second,
		ConnectRetryCount: 2,
	})
}
