---
layout: post
date: 2018-11-16  00:00:00
categories: APIConnect
title: Custom Certs in API Connect 2018
---

Custom Certs in API Connect 2018 
================================

 
When generating your own certificates for use with API connect you need
to ensure the x509 extension options are correctly set.


 
 
 

------------------------------------------------------------------------


 
 
### Custom Certs in API Connect 2018 

![](https://cdn-images-1.medium.com/max/600/0*zRF-4_vZpkunUNXo.png)

When generating your own certificates for use with API connect you need
to ensure the x509 extension options are correctly set.

Adrian Osadcenco, Chris Twomey and Michael O'Sullivan put together this
script which i have been using. The script generates all the required
certificates that can then be used during the configuration.

This script below was used for appliances (OVAs) and so all of the
management endpoints are set to to the same address

``` 
#!/bin/bash
```

``` 
#Global variables
MGMT=management-appliance.ibm.com
ANALYTISCLIENT=analytics-client-appliance.ibm.com
ANALYTICSINGESTION=analytics-ingestion-appliance.ibm.com
PORTAL_ADMIN=portal-admin-appliance.ibm.com
PORTALURL=portal-appliance.ibm.com
```

``` 
# Root Key
openssl genrsa -out rootCA.key 4096
# Root CA
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt -subj "/C=IE/ST=Cork/O=cloud, Inc./CN=gdsgdfgdf"
```

``` 
#variables
VAR_SUBJ[1]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[1]=platform-api
VAR_EXT[1]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[2]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[2]=consumer-api
VAR_EXT[2]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[3]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[3]=api-manager-ui
VAR_EXT[3]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[4]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[4]=cloud-admin-ui
VAR_EXT[4]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[5]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[5]=portal-admin-ingress
VAR_EXT[5]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[6]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[6]=portal-www-ingress
VAR_EXT[6]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[7]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[7]=analytics-client-ingress
VAR_EXT[7]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[8]="/C=IE/ST=Cork/O=cloud, Inc./CN=$"
VAR_KEY[8]=analytics-ingestion-ingress
VAR_EXT[8]="\n[SAN]\nsubjectAltName=DNS:$,DNS:$\nextendedKeyUsage=serverAuth"
```

``` 
VAR_SUBJ[9]="/C=IE/ST=Cork/O=cloud, Inc./CN=portal-client"
VAR_KEY[9]=portal-client
VAR_EXT[9]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
```

``` 
VAR_SUBJ[10]="/C=IE/ST=Cork/O=cloud, Inc./CN=analytics-ingestion-client"
VAR_KEY[10]=analytics-ingestion-client
VAR_EXT[10]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
```

``` 
VAR_SUBJ[11]="/C=IE/ST=Cork/O=cloud, Inc./CN=analytics-client-client"
VAR_KEY[11]=analytics-client-client
VAR_EXT[11]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
```

``` 
# VAR_SUBJ[9]="/C=IE/ST=Cork/O=cloud, Inc./CN=gw.192.168.151.22.nip.io"
# VAR_KEY[9]=api-gateway-ingress
# VAR_EXT[9]="\nsubjectAltName=DNS:gw.192.168.151.22.nip.io,DNS:gw.192.168.151.22.nip.io\nextendedKeyUsage=serverAuth"
#
# VAR_SUBJ[10]="/C=IE/ST=Cork/O=cloud, Inc./CN=gwd.192.168.151.22.nip.io"
# VAR_KEY[10]=api-gateway-service-ingress
# VAR_EXT[10]="\nsubjectAltName=DNS:gwd.192.168.151.22.nip.io,DNS:gwd.192.168.151.22.nip.io\nextendedKeyUsage=serverAuth"
#main
```

``` 
i=1
while [ $i -le $ ]; do
  echo --  $]} --
  echo --  $]} --
  echo --  $]} --
  openssl genrsa -out $]}.key 2048
  if [ $? != 0 ] ; then exit 1 ; fi
  # openssl req -new -sha256 -key $]}.key -subj $]} -out $]}.csr
  openssl req -new -sha256 -key $]}.key -subj "$]}" -out $]}.csr
  if [ $? != 0 ] ; then exit 1 ; fi
   openssl x509 -req -in $]}.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out $]}.crt -days 500 -sha256 -extfile <(cat /etc/ssl/openssl.cnf <(printf "$]}")) -extensions SAN
  if [ $? != 0 ] ; then exit 1 ; fi
  let i+=1
done
```





By [Chris Phillips](https://medium.com/@cminion) on
[November 16, 2018](https://medium.com/p/c7aacecd7b44).

[Canonical
link](https://medium.com/@cminion/custom-certs-in-api-connect-2018-c7aacecd7b44)

Exported from [Medium](https://medium.com) on April 6, 2019.
