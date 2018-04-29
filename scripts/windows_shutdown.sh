#!/bin/sh
# Shutdown script

ipaddress=$1
user=$2
password=$3

# echo $1
# echo $ipaddress
# echo $2
# echo $user
# echo $3
# echo $password

net rpc shutdown --comment "Shutdown request from openHAB..." --force -I $ipaddress -U $user%$password