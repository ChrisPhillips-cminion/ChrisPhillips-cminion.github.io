---
layout: post
date: 2019-08-10 02:00:00
categories: VMWare
title: "Quick Note: Making a bootable USB to install  Vmware ESXI "
---

VMWARE ESXI is a free VMWare hosting system. The primary differences between this and the full vSphere are support, limit to one host and no of supported cpus.

*TLDR* : Use RUFUS on Windows not DD or anything else.
<!--more-->

In order to install it you need to download an ISO burn it to a USB and install it on boot like a new OS.

The list of errors i saw were.

* USB not booting
* Failed to load COM32 file mboot.c32
* Menu.c32: not a COM32R error when trying to install

After multiple disks, multiple images lots of swearing using DD and Etcher I did a hail mary. I installed a Windows VM and used (Rufus)[https://rufus.ie].

!(Rufus Icon)[/images/rufus.png]

The only way I got this Working. Rufus is a Windows only ISO to USB tool. When I tried with etcher or DD it did not create a bootable USB or had issues with Syslinux.  To run this on a Mac I had to install Windows into VMWareFusion and go from there.

Yes this is a crappy solution if you are not a Windows user, it was even more crappy when i decided to move away from VMWare to Poxmon two hours later because I had two hosts... Post on this coming shortly.  
