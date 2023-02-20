# OS installation

Using the official Raspberry Pi imager application, input the following
configuration:

```yml
os: RASPBERRY OS LITE 64BIT
hostname: $HOSTNAME
enable SSH: password auth
username and password:
  username: pi
  password: "1234"
set locale settings:
  timezone: europe/madrid
  keyboard layout: es
```

# K3s installation

## Master node

```sh
sudo apt update
sudo apt install -y vim git

sudo echo -n ' cgroup_enable=memory cgroup_memory=1' >> /boot/cmdline.txt
echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> .bashrc
sudo reboot
```
