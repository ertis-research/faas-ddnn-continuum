#!/bin/bash

set -ex

curl -sfL https://get.k3s.io | sh - 
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> /home/pi/.bashrc
sudo reboot

