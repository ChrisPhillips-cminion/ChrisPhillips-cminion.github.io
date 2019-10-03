---
layout: post
date: 2019-10-03 02:00:00
categories: OpenShift
title: "MiniShift - Notes for installation"
Location: "Paris, France"
author: ["MarkTayler"]
draft: true
---
Notes shamelessly stolen from Mark Tayler for installing Mini Shift
<!--more-->
### Introduction
[`Minishift`](https://docs.okd.io/latest/minishift/index.html) is `minikube`'s equivalent for OpenShift. It can be installed locally on most operating systems.


### Installation
#### On macOS
**Note:** These steps assume that you have already installed `Homebrew` and `Docker Desktop Community`.
- You need a hypervisor and if you have Docker Desktop you will already have `hyperkit`. However, you will need to [install docker-machine-driver-hyperkit](https://docs.okd.io/latest/minishift/getting-started/setting-up-virtualization-environment.html#setting-up-hyperkit-driver) in addition to this (just `brew install docker-machine-driver-hyperkit`).
- `Homebrew` will give you some additional commands to execute during the install from the previous step that I did that before going any further. These are:
```
sudo chown root:wheel /usr/local/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
sudo chmod u+s /usr/local/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
brew services start docker-machine
```
- You can now install `Minishift` using `brew cask install minishift`.
- Start `Minishift` using `minishift start --vm-driver=hyperkit`.


### Once installed...
After starting minishift, watch out for where it tells you how to access the web console, and how to log on...
Example...
```
Server Information ...
OpenShift server started.
The server is accessible via web console at:
    https://192.168.64.2:8443/console
You are logged in as:
    User:     developer
    Password: <any value>
To login as administrator:
    oc login -u system:admin
```
For some reason, when I did a `minishift stop` followed by a `minishift start`, it did not repeat the information about who I was logged in as, or how to log in as administrator. You should probably make a note of those details.
You can gain access to the **CLI** by executing `eval $(minishift oc-env)`.
You might want to try out the [Quickstart](https://docs.okd.io/latest/minishift/getting-started/quickstart.html) to prove everything works.


#### On Windows
Take a look at https://blog.openshift.com/installing-oc-tools-windows/.
---
### When things go wrong!
#### Installing (Geraint)
The install was failing for me with a number of different errors. I forgot to make note of them at the time. One of the failures was something about not being able to find the VM's IP address in a DHCP leases file. That led me to this [Minikube issue](https://github.com/kubernetes/minikube/issues/4206).
Following the instructions in there, substituting "Minikube" with "Minishift", I was able to get it to install and start.
```
$ minishift stop
$ minishift delete
$ rm -fr ~/.minishift
$ minishift config set vm-driver hyperkit
```
The output from that last command was...
```
No Minishift instance exists. New 'vm-driver' setting will be applied on next 'minishift start'
```
When I restarted minishift (`minishift start`), it re-downloaded everything, and eventually started.
Note, even though I _do_ have Docker Desktop installed, I _did_ run `brew install hyperkit`. Also, I tried a number of `brew cask uninstall` and `brew uninstall`, none of which made any difference.
