#!/bin/bash
i=1
while true
#for ((i=1;i<=100;i++));
do
snmpwalk -v 2c -c public 192.168.10.250  1.3.6.1.2.1.1.$i 192.168.10.250;
let "i+=1"
done
