#!/bin/bash -e
### BEGIN INIT INFO
# Provides:          friendlyelec
# Required-Start:
# Required-Stop:
# Default-Start:
# Default-Stop:
# Short-Description:
# Description:       Init Onboard LEDs
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

SYS_LED=/sys/class/leds/sys_led

WAN=eth0
WAN_LED=/sys/class/leds/wan_led

LAN=tailscale0
LAN_LED=/sys/class/leds/lan1_led

WL_LED=/sys/class/leds/lan2_led

MODEL=$(tr -d '\0' </proc/device-tree/board/model)
BOARD=$(echo "${MODEL// /-}" | awk '{print tolower($0)}')

if [ -d ${SYS_LED} ]; then
    echo default-on >${SYS_LED}/trigger
fi

if [ -d ${WAN_LED} ]; then
    echo netdev >${WAN_LED}/trigger
    echo ${WAN} >${WAN_LED}/device_name
    echo 1 >${WAN_LED}/link
fi

if [ -d ${LAN_LED} ]; then
    echo netdev >${LAN_LED}/trigger
    echo ${LAN} >${LAN_LED}/device_name
    echo 1 >${LAN_LED}/link
fi

if [ -d ${WL_LED} ]; then
    echo heartbeat >${WL_LED}/trigger
fi
