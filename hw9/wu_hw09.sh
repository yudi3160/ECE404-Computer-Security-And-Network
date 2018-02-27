#! /bin/bash

##clean filter table
iptables -t filter -F
iptables -t filter -X
iptables -t nat -F
iptables -t nat -X

##place no restrictions on outbound packets
iptables -A OUTPUT -j ACCEPT

##block list of specific ip addresses
iptables -A INPUT -s 128.46.75.61 -j DROP
iptables -A INPUT -s 128.46.75.62 -j DROP
iptables -A INPUT -s 128.46.75.63 -j DROP
iptables -A INPUT -s 128.46.75.64 -j DROP
iptables -A INPUT -s 128.46.75.65 -j DROP

##block ohter computers ping my computer
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

##port-forawrding 
iptables -t nat -A PREROUTING -p tcp  -d 10.211.55.3 --dport 8005 -j DNAT --to-destination 10.211.55.3:22

##Only allow ecn.purdue.edu for SSH access
iptables -A INPUT -s ecn.purdue.edu -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j REJECT

##ONLY single IP access machine for the http service
iptables -A INPUT -p tcp -s 10.186.47.211 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j REJECT

#Permit Auth/Iden packets  on port 113
iptables -A INPUT -p tcp --dport 113 -j ACCEPT
