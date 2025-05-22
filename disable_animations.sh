#!/bin/bash

echo "[+] Desativando animações..."

# XFCE
xfconf-query -c xsettings -p /Net/EnableEventSounds -s false 2>/dev/null
xfconf-query -c xfwm4 -p /general/use_compositing -s false 2>/dev/null

# GNOME
gsettings set org.gnome.desktop.interface enable-animations false 2>/dev/null

# MATE
gsettings set org.mate.interface enable-animations false 2>/dev/null

echo "[✓] Animações e efeitos visuais desativados!"
