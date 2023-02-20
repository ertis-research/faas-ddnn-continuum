#!/bin/bash

# NODE=192.168.49.183
# ssh -t -o "StrictHostKeyChecking=no" pi@$NODE 'sudo bash -s' < docs/rpi/scripts/k3s-slave.sh
set -ex

export K3S_URL="https://192.168.49.179:6443"
export K3S_TOKEN='K1026cbde9117cd29ae24b3da61b5f924e791fbe26d5e600f4323a1df300114d7ea::server:b57bb88e1ef0c9601ca34309e41dbbcf'

curl -sfL https://get.k3s.io | sh - 
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> /home/pi/.bashrc
# k3s agent --server "${K3S_URL}" --token "${NODE_TOKEN}"
reboot
