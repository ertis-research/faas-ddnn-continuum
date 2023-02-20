### Node password rejected, duplicate hostname

```sh
$ sudo journalctl -u k3s-agent
Feb 20 11:21:01 ertis5 k3s[551]: time="2023-02-20T11:21:01+01:00" level=info msg="Waiting to retrieve agent configuration; server is not ready: Node password rejected, duplicate hostname or contents of '/etc/rancher/node/password' may not match server node-passwd entry, try enabling a unique node name with the --with-node-id flag"
```

- https://blog.codybunch.com/2020/10/13/Kubernetes-Fix-Node-Password-Rejected/
- /var/lib/rancher/k3s/server/cred/node-passwd moved to
  /etc/rancher/node/password
- `kubectl delete secrets -n kube-system <NODE>.node-password.k3s`
