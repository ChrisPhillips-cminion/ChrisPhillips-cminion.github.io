---
layout: post
categories: APIConnect
date: 2020-11-13 00:14:00
title: Custom SSL Certificates on API Connect V10.
---

We recommend that each customer uses their own SSL Certificates signed with their own CA. These instructions will show a script to generate and load all certificates as well as instructions for rolling your own.

<!--more-->


**TLDR:** This script will generate all required CAs and certificates and load them into Kubernetes. Please note that the subj for the analytics client certificates must be `"/O=cert-manager/CN="`.


<button class="collapsible" id="fulloutput">Shell script to generate and load all certificates</button>

<div class="content" id="fulloutputdata" markdown="1">
```bash
MGMT=admin.apic-playground.eu-gb.containers.appdomain.cloud
MGMT2=manager.apic-playground.eu-gb.containers.appdomain.cloud
MGMT3=api.apic-playground.eu-gb.containers.appdomain.cloud
MGMT4=consumer.apic-playground.eu-gb.containers.appdomain.cloud
ANALYTICSCLIENT=ac.apic-playground.eu-gb.containers.appdomain.cloud
ANALYTICSINGESTION=ai.apic-playground.eu-gb.containers.appdomain.cloud
PORTAL_ADMIN=api.portal.apic-playground.eu-gb.containers.appdomain.cloud
PORTALURL=portal.apic-playground.eu-gb.containers.appdomain.cloud
ns=apic
SUBJ="/O=cert-manager/CN="
​
​
# Root Key
openssl genrsa -out ca.key 4096
# Root CA
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.crt -subj ${SUBJ}dsgdfgdf
kubectl create secret tls ingress-ca --key ca.key --cert ca.crt -n $ns
​
#variables
VAR_SUBJ[1]=$SUBJ
VAR_KEY[1]=api-endpoint
VAR_EXT[1]="\n[SAN]\nsubjectAltName=DNS:$MGMT3,DNS:$MGMT3\nextendedKeyUsage=serverAuth"
VAR_SUBJ[2]=$SUBJ
VAR_KEY[2]=consumer-endpoint
VAR_EXT[2]="\n[SAN]\nsubjectAltName=DNS:$MGMT4,DNS:$MGMT4\nextendedKeyUsage=serverAuth"
VAR_SUBJ[3]=$SUBJ
VAR_KEY[3]=apim-endpoint
VAR_EXT[3]="\n[SAN]\nsubjectAltName=DNS:$MGMT2,DNS:$MGMT2\nextendedKeyUsage=serverAuth"
VAR_SUBJ[4]=$SUBJ
VAR_KEY[4]=cm-endpoint
VAR_EXT[4]="\n[SAN]\nsubjectAltName=DNS:$MGMT,DNS:$MGMT\nextendedKeyUsage=serverAuth"
​
​
VAR_SUBJ[5]=$SUBJ
VAR_KEY[5]=portal-admin
VAR_EXT[5]="\n[SAN]\nsubjectAltName=DNS:$PORTAL_ADMIN,DNS:$PORTAL_ADMIN\nextendedKeyUsage=serverAuth"
VAR_SUBJ[6]=$SUBJ
VAR_KEY[6]=portal-web
VAR_EXT[6]="\n[SAN]\nsubjectAltName=DNS:$PORTALURL,DNS:$PORTALURL\nextendedKeyUsage=serverAuth"
VAR_SUBJ[7]=$SUBJ
VAR_KEY[7]=analytics-ac-endpoint
VAR_EXT[7]="\n[SAN]\nsubjectAltName=DNS:$ANALYTICSCLIENT,DNS:$ANALYTICSCLIENT\nextendedKeyUsage=serverAuth"
VAR_SUBJ[8]=$SUBJ
VAR_KEY[8]=analytics-ai-endpoint
VAR_EXT[8]="\n[SAN]\nsubjectAltName=DNS:$ANALYTICSINGESTION,DNS:$ANALYTICSINGESTION\nextendedKeyUsage=serverAuth"
​​
VAR_SUBJ[9]=$SUBJ
VAR_KEY[9]=portal-admin-client
VAR_EXT[9]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
VAR_SUBJ[10]=$SUBJ
VAR_KEY[10]=analytics-ingestion-client
VAR_EXT[10]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
VAR_SUBJ[11]=$SUBJ
VAR_KEY[11]=analytics-client-client
VAR_EXT[11]="\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n"
​
​
#main
i=1
while [[ $i -le 11 ]]; do
  echo --  ${VAR_SUBJ[$i]} --
  echo --  ${VAR_KEY[$i]} --
  echo --  ${VAR_EXT[$i]} --
  openssl genrsa -out ${VAR_KEY[$i]}.key 2048
  if [ $? != 0 ] ; then exit 1 ; fi
  # openssl req -new -sha256 -key $]}.key -subj $]} -out $]}.csr
  openssl req -new -sha256 -key ${VAR_KEY[$i]}.key -subj "${VAR_SUBJ[$i]}${VAR_KEY[$i]}" -out ${VAR_KEY[$i]}.csr
  cat /etc/ssl/openssl.cnf > tmp.cnf
  echo ${VAR_EXT[$i]} >> tmp.cnf
  echo ${VAR_EXT[$i]} > tmp2.cnf
  if [ $? != 0 ] ; then exit 1 ; fi
  openssl x509 -req -in ${VAR_KEY[$i]}.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ${VAR_KEY[$i]}.crt -days 500 -sha256 -extfile <(cat /etc/ssl/openssl.cnf <(printf "${VAR_EXT[$i]}")) -extensions SAN
cat >ksec.yaml <<EOF
apiVersion: v1
data:
  ca.crt: $(base64   ca.crt | tr -d '\n' )
  tls.crt: $(base64  ${VAR_KEY[$i]}.crt | tr -d '\n' )
  tls.key: $(base64   ${VAR_KEY[$i]}.key | tr -d '\n' )
kind: Secret
metadata:
  name:  ${VAR_KEY[$i]}
type: kubernetes.io/tls
EOF
  if [ $? != 0 ] ; then exit 1 ; fi
  kubectl apply -f ksec.yaml -n$ns
  if [ $? != 0 ] ; then exit 1 ; fi
  let i+=1
done
```
</div>



The following certificates must be generated
* api-endpoint
* consumer-endpoint
* apim-endpoint
* cm-endpoint
* portal-admin
* portal-web
* analytics-ac-endpoint
* analytics-ai-endpoint

Plus the following client certificates
* analytics-ingestion-client
* analytics-client-client
* portal-admin-client

Once these are generated they will need to referenced in the CRs prior to applying them.   

To generate a new CA if one is not available run the following command

```bash
openssl genrsa -out ca.key 4096
# Root CA
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1024 -out ca.crt -subj cn=apic-ca
```

For the following commands we are assuming the file names match what was used in the previous lines.

For each certificate the following command is run replacing `<certname>` with the certificate name and `<Host>` with the endpoint for that component

```bash
openssl genrsa -out <certname>.key 2048
openssl genrsa -out <certname>.key 2048openssl req -new -sha256 -key <certname>.key -subj "/O=cert-manager/CN=<certname>" -out <certname>.csr
openssl x509 -req -in <certname>.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out <certname>.crt -days 500 -sha256 -extfile <(cat /etc/ssl/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:<HOST>,DNS:<HOST>\nextendedKeyUsage=serverAuth")) -extensions SAN
```

For the client certificates we require the following commands

```base
openssl genrsa -out <certname>.key 2048
openssl genrsa -out <certname>.key 2048openssl req -new -sha256 -key <certname>.key -subj "/O=cert-manager/CN=<certname>" -out <certname>.csr
openssl x509 -req -in <certname>.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out <certname>.crt -days 500 -sha256 -extfile <(cat /etc/ssl/openssl.cnf <(printf "\n[SAN]\nkeyUsage=critical, digitalSignature, keyEncipherment\nextendedKeyUsage = clientAuth\nbasicConstraints=critical, CA:FALSE\nsubjectKeyIdentifier=hash\n")) -extensions SAN
```


We must load the cert and key with the CA into secrets in kubernetes, where <namespace> is the namespace you will deploy APIC.

```bash
cat >ksec.yaml <<EOF
apiVersion: v1
data:
  ca.crt: $(base64   ca.crt | tr -d '\n' )
  tls.crt: $(base64  <certname>.crt | tr -d '\n' )
  tls.key: $(base64   <certname>.key | tr -d '\n' )
kind: Secret
metadata:
  name:  <certname>
type: kubernetes.io/tls
EOF
kubectl apply -f ksec.yaml -n <namespace>
```


Now validate that the certificates are corretly referenced in the CRs and apply them.
