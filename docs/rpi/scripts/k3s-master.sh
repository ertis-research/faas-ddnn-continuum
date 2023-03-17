#!/bin/bash

# ssh -t -o "StrictHostKeyChecking=no" iertis1 'sudo bash -s' < docs/rpi/scripts/k3s-master.sh
set -ex

curl -sfL https://get.k3s.io | sh - 
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> /home/pi/.bashrc
sudo reboot

