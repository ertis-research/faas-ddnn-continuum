### Install ERTIS certificate on all machines

```sh
docs/rpi/scripts/exec.sh "
echo '
mirrors:
  \"192.168.43.7:30501\":
    endpoint:
      - \"https://192.168.43.7:30501\"
configs:
  \"192.168.43.7:30501\":
    tls:
      ca_file: /usr/local/share/ca-certificates/ertis-ca.crt
' > /tmp/registries.yaml
sudo mkdir -p /etc/rancher/k3s/
sudo cp /tmp/registries.yaml /etc/rancher/k3s/registries.yaml"

docs/rpi/scripts/exec.sh "echo '-----BEGIN CERTIFICATE-----
MIIBfDCCASKgAwIBAgIQI/l98T6YFgV3Yon4j5/9YTAKBggqhkjOPQQDAjAeMRww
GgYDVQQDExNlcnRpcy1zZWxmc2lnbmVkLWNhMB4XDTIzMDIxNDEwMTEwMloXDTIz
MDUxNTEwMTEwMlowHjEcMBoGA1UEAxMTZXJ0aXMtc2VsZnNpZ25lZC1jYTBZMBMG
ByqGSM49AgEGCCqGSM49AwEHA0IABJr6yBE9dwtbVC6wIGLaxTgEidXZ29DQxapL
8KYfUDhvY6CjsYKCB1YzGiBgaIWkse0Kdr4iUsldv8hsVz3/FsmjQjBAMA4GA1Ud
DwEB/wQEAwICpDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRSVtgUTcSMBpf7
rSueTV7t/f1yADAKBggqhkjOPQQDAgNIADBFAiEAoRsUXzeDuRqyphhCxrKQWsSm
LCPIygliNeVxVj7sxs4CIHiIzuRc085L3YwU54XTf45Rku8Gw3bYZiPoiQPZkNXV
-----END CERTIFICATE-----' > /tmp/ertis-ca.crt
sudo mv /tmp/ertis-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates"

docs/rpi/scripts/exec.sh sudo reboot
```

### Enable pod eviction if nodes aren't available

```sh
docs/rpi/scripts/exec.sh "echo '
kubelet-arg: node-status-update-frequency=4s
kube-controller-manager-arg:
  - node-monitor-period=4s
  - node-monitor-grace-period=16s
  - pod-eviction-timeout=20s
kube-apiserver-arg:
  - default-not-ready-toleration-seconds=20
  - default-unreachable-toleration-seconds=20
' > /tmp/config.yaml
sudo mv /tmp/config.yaml /etc/rancher/k3s/config.yaml
"
docs/rpi/scripts/exec.sh sudo reboot
```
