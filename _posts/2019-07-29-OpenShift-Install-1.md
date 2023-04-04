---
layout: post
date: 2019-07-28 12:00:00
categories: OpenShift
title: "Installing OpenShift 3.11  Again Part - 1"
draft: true
---
<!--more-->
_So Jeff has gone to a better place. My many year old ATOM that I was using as one of the nodes and bootstrap server for OpenShift 3.11. Its CPU was clocked at 80'c and then overnight it never returned._

Jeff held my inventory file (config file) for my OpenShift and with the passing off Jeff (and his disk) I have lost the file and all notes I had made.

The purpose of this series of Articles is to document my install process of OKD on Fedora 29 (Linux distro). OKD is the OpenSource version of OpenShift.  I want OKD over K8s or K3s because it is the K8s platform of choice by all big businesses.  However as I have stated many many times before I am not an infra guy. I am happier at the application layer and above.

I will document hopefully using ASCIINEMA everything I do in the  hope that it will help someone else hitting these same issues.

My environment will consist of
| | Description | OS |
| --- | --- | --- |
| random |  32GB Ram 16 vCPU - Master, Compute, Infra | Fedora 29 Workstation  |
| banana |  32GB Ram 8 vCPU - Compute | Fedora 29 Server  |
| randomstore |  8GB (16gb When i find some RAM) RAM 4 vCPU, Compute | Fedora 29 Server  |

This is NOT an HA environment, as much as I would like an HA environment I cannot get away with any more machines being on 24/7


I have got SSH Keys working between the environments and correctly set up the hostnames.


I have cloned the ansible playbook repository to /opt/src and checked out 3.11


This is my initial inventory file that I have put into /etc/ansible/hosts

<button class="collapsible" id="yaml">Inv File</button>
<div class="content" id="yamldata" markdown="1">
```
# Create an OSEv3 group that contains the masters, nodes, and etcd groups
[OSEv3:children]
masters
nodes
etcd
glusterfs

# Set variables common for all OSEv3 hosts
[OSEv3:vars]
# SSH user, this user should allow ssh based auth without requiring a password
ansible_ssh_user=root
# If ansible_ssh_user is not root, ansible_become must be set to true
#ansible_become=true
openshift_deployment_type=origin

# uncomment the following to enable htpasswd authentication; defaults to AllowAllPasswordIdentityProvider
#openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider'}]

# host group for masters
[masters]
random.phillips11.cf

# host group for etcd
[etcd]
random.phillips11.cf

# host group for nodes, includes region info
[nodes]
random.phillips11.cf OpenShift_node_group_name='node-config-all-in-one' ansible_python_interpreter='/usr/bin/python3' OpenShift_schedulable=True
randomstore.phillips11.cf OpenShift_node_group_name='node-config-compute' OpenShift_schedulable=True ansible_python_interpreter=/usr/bin/python3
banana.phillips11.cf OpenShift_node_group_name='node-config-compute' OpenShift_schedulable=True ansible_python_interpreter=/usr/bin/python3

[nodes:vars]
ansible_python_interpreter='/usr/bin/python3'

[glusterfs]
random.phillips11.cf glusterfs_devices='[ "/dev/fedora/gfs" ]'
banana.phillips11.cf glusterfs_devices='[ "/dev/fedora_banana/gfs" ]'
randomstore.phillips11.cf glusterfs_devices='[ "/dev/fedora/gfs" ]'
```
</div>

The video of the PreReq running is available here.

[![asciicast](https://asciinema.org/a/PJEfB2FbDvyCtxFUq5HqBcMkb.svg)](https://asciinema.org/a/PJEfB2FbDvyCtxFUq5HqBcMkb)
