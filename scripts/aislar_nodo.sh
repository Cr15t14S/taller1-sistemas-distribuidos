#!/bin/bash
# Script para simular particion de red aislando el nodo en Tailscale
sudo iptables -A INPUT -i tailscale0 -j DROP
sudo iptables -A OUTPUT -o tailscale0 -j DROP
echo "Nodo aislado exitosamente de la red tailscale0."
