#!/bin/bash
# Script para restablecer la conexion en Tailscale
sudo iptables -D INPUT -i tailscale0 -j DROP
sudo iptables -D OUTPUT -o tailscale0 -j DROP
echo "Conexion restablecida en la interfaz tailscale0."
