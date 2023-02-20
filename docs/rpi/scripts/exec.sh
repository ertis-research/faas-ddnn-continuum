#!/bin/zsh

ertis_ip_addr=( 192.168.49.{179..182} )

for IP in $ertis_ip_addr
do 
    HOST="pi@$IP"
    (eval $* |& sed "s/^/$IP: /g" ) &
done

wait