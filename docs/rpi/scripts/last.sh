#!/bin/bash
set -ex

# ssh -t -o "StrictHostKeyChecking=no" pi@rpi-builder 'sudo bash -s' < docs/rpi/scripts/first.sh

# Disable wifi and bluetooth
sudo rfkill block wifi
sudo rfkill block bluetooth