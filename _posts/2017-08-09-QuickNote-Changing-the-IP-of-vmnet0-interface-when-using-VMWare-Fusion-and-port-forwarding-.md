---
layout: post
date: 2017-08-09  00:00:00
categories: APIConnect
title: |
    QuickNote: Changing the IP of vmnet0 interface when using VMWare Fusion
    and port forwarding.
---

QuickNote: Changing the IP of vmnet0 interface when using VMWare Fusion and port forwarding.
============================================================================================


So if you need to change the vmnet1 or vmnet8 ipaddress edit the
following file






------------------------------------------------------------------------




### QuickNote: Changing the IP of vmnet0 interface when using VMWare Fusion and port forwarding.

So if you need to change the vmnet1 or vmnet8 ipaddress edit the
following file

```
sudo vi /Library/Preferences/VMware\ Fusion/networking
```

this will look like the following

```
VERSION=1,0
answer VNET_1_DHCP yes
answer VNET_1_DHCP_CFG_HASH 874589F453D90B947397E10B3C9FAEE31AD6691B
answer VNET_1_HOSTONLY_NETMASK 255.255.255.0
answer VNET_1_HOSTONLY_SUBNET 172.16.231.0
answer VNET_1_VIRTUAL_ADAPTER yes
answer VNET_8_DHCP yes
answer VNET_8_DHCP_CFG_HASH D1762C98F83DCFA2FE8248DF20B4FF9B92F24A0D
answer VNET_8_HOSTONLY_NETMASK 255.255.255.0
answer VNET_8_NAT yes
answer VNET_8_VIRTUAL_ADAPTER yes
add_nat_portfwd 8 tcp 444 192.168.42.104 444
add_nat_portfwd 8 tcp 8080 172.16.3.128 80
```

Look at line

```
answer VNET_8_HOSTONLY_SUBNET 192.168.42.0
```

Set the hostonly subnet you require by changing the first three sets of
numbers.

If you need to add port forwarding then add lines like the following

```
add_nat_portfwd 8 tcp 444 192.168.42.104 444
```

This will route any traffic to my host machine on port 444 to the vm on
192.168.42.104 port 444.

Once you have made the changes you require you must run the following
three commands.

```
sudo /Applications/VMware Fusion.app/Contents/Library/vmnet-cli --configure
sudo /Applications/VMware Fusion.app/Contents/Library/vmnet-cli --stop
sudo /Applications/VMware Fusion.app/Contents/Library/vmnet-cli --start
```

*(Commands above taken from*
[*https://vbrownbag.com/2014/03/restart-vmware-fusion-networking-from-the-command-line/*](https://vbrownbag.com/2014/03/restart-vmware-fusion-networking-from-the-command-line/) *to save me looking in my bash history)*





By [Chris Phillips](https://medium.com/@cminion) on
[August 9, 2017](https://medium.com/p/983f3d9011f7).

[Canonical
link](https://medium.com/@cminion/quicknote-changing-the-ip-of-vmnet0-interface-when-using-vmware-fusion-983f3d9011f7)

Exported from [Medium](https://medium.com) on April 6, 2019.
