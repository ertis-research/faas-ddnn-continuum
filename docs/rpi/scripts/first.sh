#!/bin/bash
set -ex

# ssh -t -o "StrictHostKeyChecking=no" pi@rpi-builder 'sudo bash -s' < docs/rpi/scripts/first.sh
export CONFIG_STATIC_IP=192.168.49.184

sudo echo -n ' cgroup_enable=memory cgroup_memory=1' >> /boot/cmdline.txt
echo "
persistent
# Generate Stable Private IPv6 Addresses instead of hardware based ones
slaac private

# static IP configuration:
interface eth0
static ip_address=${CONFIG_STATIC_IP}/23
# static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.49.252
static domain_name_servers=1.1.1.1
# 192.168.42.3 150.214.40.11
" > /tmp/dhcpcd.conf
cp /tmp/dhcpcd.conf /etc/dhcpcd.conf

# See https://github.com/k3s-io/k3s/issues/703#issuecomment-522355829
sudo iptables -F
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy

shutdown -h now
