#!/bin/bash
password=$1
disk=$2
type=$3
if [ $type == filesystem ]
then
    echo $password | sudo -S umount -l /dev/vd$disk
    echo $password | sudo -S mkfs.ext4 /dev/vd$disk
    echo $password | sudo -S mkdir -p /mnt/vd$disk
    echo $password | sudo -S mount -o sync /dev/vd$disk /mnt/vd$disk
else
    echo $password | sudo -S umount -l /dev/vd$disk
fi
