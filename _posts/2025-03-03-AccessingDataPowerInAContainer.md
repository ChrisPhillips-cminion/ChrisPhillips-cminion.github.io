---
layout: post
date: 2025-03-03 09:00:00
categories: IBM DataPower
title: "Accessing the IBM DataPower interface in a container"
author: [ "ChrisPhillips", "IvanH" ]
draft: true
---

When accessing IBM DataPower in a container we recommend it is  accessed via the CLI. However, if there is a lot of traffic in the IBM DataPower this can make it difficult to follow as the log messages are sent to the screen.

<!--more-->

A better way is to enable telnet on the local interface and exec into the IBM DataPower pod and telnet into the application. Todo this create the following config as a ConfigMap

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

**edit GatewayCluster**
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

And even run more complex commands against multiple pods with commands like

```
for gw in `oc -n cp4i get pods |grep gw|awk '{print $1}'`
do
  echo $gw
 kubectl -n cp4i  exec -it $gw --  nc 127.0.0.1 2300 < sh-peering-status.txt |strings
done
```

Where sh-peering-status.txt contains with password replaced with the gw password
```
admin
password
top;co;sw apiconnect;sh gateway-peering-st
exit
exit
```
