---
layout: post
categories: GraphQL
date: 2021-02-08 00:14:00
title: Configuring a Gateway in a different cloud.
draft: true
---

API Connect declaires itself as the first API Management solution to support multi cloud deployments. This is where you can deploy each part of a the API Cloud into a different cloud, if required. This article will go through the steps to configure a DataPower in Kubernetes that can be configured to work with an API Manager that is in another cloud.

<!--more-->
### Assumptions
1. You have a Kubernetes or OpenShift environment running to deploy the DataPower
2. You have deployed the IBM DataPower operator into this cluster
3. You have deployed cert manager (k8s) or IBM common services (OpenShift) into this cluster
4. You an API Manager available, RI, OVA, Kubernetes or Openshift.
5. You are not prepared to export the CA Key from the API Manager to loading into the certman in the DataPower Cluster. (We recommend you do NOT do this as it is a security risk.)

**Thanks to John Bellessa for the help finding this out.**

### Steps
1 Extract the CA from the API manager endpoint and rename it to `api-manager.crt`
2 Add the CA into a secret using the following command
`kubectl create secret generic apimanager-ca --from-file=./api-manager.crt`
3 Create the following dp-configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gwd-add-apimgmt-ca
data:
  gwd_client.cfg: |
    crypto
    certificate gwd_client_valcred_ca cert:///api-manager.crt
    valcred gwd_client_valcred ; certificate gwd_client_valcred_ca ; exit
    ssl-client gwd_client
      validate-server-cert on
      valcred gwd_client_valcred
    exit
    exit
```
4 Apply the config ConfigMap
`kubectl apply -f  dp-configmap.yaml`

5 Save save the gateway cr below into a file called `gateway-cr.yaml`. Please update all variables as detailed in the API Connect Knowledge center [https://www.ibm.com/support/knowledgecenter/SSMNED_v10/com.ibm.apic.install.doc/tapic_v10_install_kubernetes_gwy.html](https://www.ibm.com/support/knowledgecenter/SSMNED_v10/com.ibm.apic.install.doc/tapic_v10_install_kubernetes_gwy.html)
```yaml
apiVersion: gateway.apiconnect.ibm.com/v1beta1
kind: GatewayCluster
metadata:
  name: gwv6
  namespace: $APIC_NAMESPACE
  labels: {
    app.kubernetes.io/instance: "gateway",
    app.kubernetes.io/managed-by: "ibm-apiconnect",
    app.kubernetes.io/name: "gwv6"
  }
spec:
  version: $APP_PRODUCT_VERSION
  profile: $GW_PROFILE
  imagePullSecrets:
  - $SECRET_NAME
  apicGatewayServiceV5CompatibilityMode: false
  gatewayEndpoint:
    annotations:
      certmanager.k8s.io/issuer: ingress-issuer
    hosts:
    - name: gw.$STACK_HOST
      secretName: gwv6-endpoint
  gatewayManagerEndpoint:
    annotations:
      certmanager.k8s.io/issuer: ingress-issuer
    hosts:
    - name: gwd.$STACK_HOST
      secretName: gwv6-manager-endpoint
  apicGatewayServiceTLS:
    secretName: gateway-service
  apicGatewayPeeringTLS:
    secretName: gateway-peering
  datapowerLogLevel: 3
  license:
    accept: $LICENSE_ACCEPT
    use: $LICENSE_USAGE
  tokenManagementService:
    enabled: true
    storage:
      storageClassName: $BLOCK_STORAGE_CLASS
      volumeSize: 30Gi
  additionalDomainConfig:
    - name: "apiconnect"
      certs:
      - certType: "usrcerts"
        secret: "apimanager-ca"
      dpApp:
        config:
        - "gwd-add-apimgmt-ca"
        local:  []
  adminUser:
    secretName: $GW_ADMIN_USER_SECRET
  syslogConfig:
    enabled: false # if true, provide below details
```
6 Apply the cr
`kubectl apply -f gateway-cr.yaml`

7 The final step is to extract the gateway client certificates and load them into the API Cloud Admin.
```bash
kubectl get secrets  gateway-client-client -o yaml > secret.yaml
grep ca.crt secret.yaml | head -1 | awk '{print $2}' | base64 -d > ca.crt
grep tls.crt secret.yaml | head -1 | awk '{print $2}' | base64 -d > tls.crt
grep tls.key secret.yaml | head -1 | awk '{print $2}' | base64 -d > tls.key
```

8 These can be loaded into a new TLS profile in the API Manager.

9 Register a new Gateway Services using the TLS Profile specified.
