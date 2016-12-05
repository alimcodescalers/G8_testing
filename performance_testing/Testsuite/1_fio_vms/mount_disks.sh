#!/bin/bash
password=$1
disk=$2
echo $password | sudo -S umount /dev/vd$disk
echo $password | sudo -S mkfs.ext4 /dev/vd$disk
echo $password | sudo -S mkdir -p /mnt/vd$disk
echo $password | sudo -S mount -o sync /dev/vd$disk /mnt/vd$disk
