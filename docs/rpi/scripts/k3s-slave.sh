#!/bin/bash

# NODE=192.168.49.183
# ssh -t -o "StrictHostKeyChecking=no" pi@$NODE 'sudo bash -s' < docs/rpi/scripts/k3s-slave.sh
set -ex

export K3S_URL="https://192.168.49.179:6443"
export K3S_TOKEN='K103bd28985a50585b741bde69862a032a9ba7a3f55a935bb65fbf5db85d1e0f6fe::server:7f0b3ccfb31c97066e175a334bddde08'

curl -sfL https://get.k3s.io | sh - 
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> /home/pi/.bashrc
# k3s agent --server "${K3S_URL}" --token "${NODE_TOKEN}"
reboot
