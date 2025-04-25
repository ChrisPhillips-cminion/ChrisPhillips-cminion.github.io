---
layout: post
date: 2025-04-25 09:00:00
categories: DataPower
title: "Accessing the IBM DataPower Command Line Interface  (CLI) in a container"
author: [ "ChrisPhillips", "IvanH" ]
---

When accessing IBM DataPower in a container we recommend it is  accessed via the CLI. However, if there is a lot of traffic in the IBM DataPower this can make it difficult to follow as the log messages are sent to the screen.

<!--more-->

A better way is to enable telnet on the local interface and exec into the IBM DataPower pod and telnet into the application. To do this create the following config as a ConfigMap

```
cat <EOF > telnet_cli_service.cfg
cli telnet "telnet_Service"
  ip-address 127.0.0.1
  port 2300
exit
EOF
oc -n apic create ConfigMap telnet-service-cm --from-file=telnet_cli_service.cfg
```

Then add the following into the Gateway Service configuration

`oc edit gw <gwname> -n apic`

```
spec:
  additionalDomainConfig:
  - dpApp:
      config:
      - telnet-service-cm
    name: default
```

This will cause the pods to restart. Once that restart is complete you can connect to the telnet session with

```
kubectl -n apic exec -it apic-gw-0  --  nc 127.0.0.1 2300
```

This can be built on to run more complex commands against multiple gw pods with commands like

```
for gw in `oc -n apic get pods |grep gw|awk '{print $1}'`
do
  echo $gw
  kubectl -n apic  exec -it $gw --  nc 127.0.0.1 2300 < sh-peering-status.txt |strings
done
```

Where sh-peering-status.txt contains the following with password replaced with the gateway password

```
admin
password
top;co;sw apiconnect;sh gateway-peering-st
exit
exit
```
