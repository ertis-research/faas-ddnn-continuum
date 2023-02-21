#!/bin/zsh

# Execute a command on all fog nodes

# kill $(jobs -p) to stop execution
ertis_ip_addr=( 192.168.49.{179..184} )

for IP in $ertis_ip_addr
do 
    (ssh -t -o "StrictHostKeyChecking=no" -o "ConnectTimeout=3" "pi@$IP" $* |& sed "s/^/[$IP]: /g" ) &
done

wait