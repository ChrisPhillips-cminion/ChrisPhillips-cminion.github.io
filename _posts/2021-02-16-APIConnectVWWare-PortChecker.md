---
layout: post
categories: APIConnect
date: 2021-02-16 00:14:00
title: Validating network connectivity of VMWare OVA deployment of API Connect
---

This article provides a script that will allow you to validate network connectivity between you VMWare Appliances.

<!--more-->



This script can be run on teach of the  API Manager, Analytics and Portal VMs.

The script will validate communication as documented by the API Connect Knowledge center. For APIConnect v10 the firewall rules are described here [https://www.ibm.com/support/knowledgecenter/SSMNED_v10/com.ibm.apic.install.doc/overview_apimgmt_portreqs_vmware.html](https://www.ibm.com/support/knowledgecenter/SSMNED_v10/com.ibm.apic.install.doc/overview_apimgmt_portreqs_vmware.html)

Please fill in the details in the export lines at the start. These need to be filled in for all environments.  It prints a summary to the screen and stores the longer error messages to a file. `errorLog-DATESTAMP.txt`

Thanks to Will Simmons for his assistance in getting me an HA test environment

**This script is provided with no support and as is.** If you find any issues please comment below and I will take a look if able.
```bash

#!/usr/bin/bash
​
#Uncomment the line depending on which VM the script is being run.
export ScriptRunningOn=API_MANAGER
# export ScriptRunningOn=API_PORTAL
# export ScriptRunningOn=API_ANALYTICS​

#if only one comment out 2 and 3
export API_MANAGER=apimdev0217.hursley.ibm.com
export API_MANAGER2=apimdev0218.hursley.ibm.com
export API_MANAGER3=apimdev0219.hursley.ibm.com
​
#Make sure you have the api endpoint
export API_MANAGER_lb=api.apimdev0216.hursley.ibm.com
​
#if only one comment out 2 and 3
export API_PORTAL=apimdev0221.hursley.ibm.com
export API_PORTAL2=apimdev0222.hursley.ibm.com
export API_PORTAL3=apimdev0223.hursley.ibm.com
​
#Make sure you have the  portal director endpoint
export API_PORTAL_DIRECTOR_lb=api.portal.apimdev0220.hursley.ibm.com
​
#if only one comment out 2 and 3
export API_ANALYTICS=apimdev0225.hursley.ibm.com
export API_ANALYTICS2=apimdev0226.hursley.ibm.com
export API_ANALYTICS3=apimdev0227.hursley.ibm.com
​
#Make sure you have the AC and AI endpoint
export API_ANALYTICS_AC_lb=ac.apimdev0224.hursley.ibm.com
export API_ANALYTICS_AI_lb=ai.apimdev0224.hursley.ibm.com
​
#Make sure you have the AC and AI endpoint
export API_GATEWAY_lb=apimdev0066.hursley.ibm.com
export API_GATEWAY_SERVICE_lb=apimdev0066.hursley.ibm.com
# The default value is 3000
export API_GATEWAY_SERVICE_port=3000

portCheck () {
  echo $(date) -  testing port $2
  echo $(date) -  testing port $2  >> errorLog-$date.txt
  host=$1
  port=$2
  resp=$(echo "QUIT" | openssl s_client -connect $host:$port -servername $host 2>/dev/null)
  result=$(echo $resp | head -n 1  | sed -e s/[^A-Z].*//)
  if [[ "$result" == "CONNECTED" ]] ; then
    echo $(date) - $host:$port CONNECTED
  else
    echo $(date) - $(hostname) to  $host:$port FAILED to connect
    echo $(date) - from $(hostname) to $host:$port FAILED to connect >> errorLog-$date.txt
    echo RUNNING   openssl s_client -connect $host:$port  -servername $host >> errorLog-$date.txt
    openssl s_client -connect $host:$port  -servername $host 2>>errorLog-$date.txt  >> errorLog-$date.txt
  fi
}
date=$(date +%s)
if [ "$ScriptRunningOn" == "API_MANAGER" ] ; then
  echo $(date) -  Validating API Manager to API Manager connectivity
  for i in 22 443 2379 2380 6443 10250 10254 10256 10257 10259  ; do
    portCheck $API_MANAGER  $i
    if [[ -n "$API_MANAGER2" ]]
    then
      portCheck $API_MANAGER2 $i
    fi
    if [[ -n "$API_MANAGER3" ]]
    then
      portCheck $API_MANAGER3 $i
    fi
  done
  # portCheck $API_GATEWAY_lb 443
  portCheck $API_GATEWAY_SERVICE_lb $API_GATEWAY_SERVICE_port
  portCheck $API_PORTAL_DIRECTOR_lb 443
  portCheck $API_ANALYTICS_AC_lb 443
  portCheck $API_ANALYTICS_AI_lb 443
fi
if [ "$ScriptRunningOn" == "API_ANALYTICS" ] ; then
  echo $(date) -  Validating Analytics to Analytics connectivity
  for i in 22 443 2379 2380 6443 10250  10254 10256 10257 10259  ; do
    portCheck $API_ANALYTICS   $i
    if [[ -n "$API_ANALYTICS2" ]]
    then
      portCheck $API_ANALYTICS2 $i
    fi
    if [[ -n "$API_ANALYTICS3" ]]
    then
      portCheck $API_ANALYTICS3 $i
    fi
  done
fi
if [ "$ScriptRunningOn" == "API_PORTAL" ] ; then
  echo $(date) -  Validating to Portal to Portal connectivity
  for i in 22 443 2379 2380 6443  10250  10254 10256 10257 10259  3009 3010 3306 3307 4443 4444 4567 4568 30865 ; do
    portCheck $API_PORTAL $i
    if [[ -n "$API_PORTAL2" ]]
    then
      portCheck $API_PORTAL2 $i
    fi
    if [[ -n "$API_PORTAL3" ]]
    then
      portCheck $API_PORTAL3 $i
    fi
  done
  portCheck $API_MANAGER_lb 443
fi
```
