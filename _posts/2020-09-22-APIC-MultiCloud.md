---
layout: post
date: 2020-9-22 00:13:00
categories: APIConnect
title: "Deploying Analytics in a different Cloud"
draft: true
---

API Connect supports deploying each of their components on different clouds and managing them from a single API Management server. This article goes through the steps on how to do this in OpenShift and Kubernetes.
​

<!--more-->

1. Install the API Connect manager and validate that you can log into the Cloud Admin console
2. Install CertMan and the API Operator into the cluster to host the remote analytics.
3. Ensure the ibm-entlitlement-key secret is in the namespace on the cluster to host the remote analytics.
4. Export the `<APIC mgmt deployment name>-ingress-ca` secret from the namespaces with API Connect Manager. _In these example `APIC mgmt deployment name` is `apic-new`._

`oc get secret -n apic apic-new-ingress-ca -ojson | jq 'del(.metadata.creationTimestamp,.metadata.namespace,.metadata.resourceVersion,.metadata.uid,.metadata.selfLink)' > ingress-secret.json`

5. Load ingress-secret.json into the desiredname space on the new cluster.

6. Put the following lines into a file call `ingress-issuer.yaml` and apply it to the namespaces on the cluster to host the remote analytics.
```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: <APIC mgmt deployment name>-ingress-issuer
spec:
  ca:
    secretName: <APIC mgmt deployment name>-ingress-ca
---
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: <APIC mgmt deployment name>-self-signed
spec:
  selfSigned: {}
```
7. run `oc apply -f ingress-issuer.yaml` to create the Issuer

8. Validate that the Issuer is in the ready state with the following command.
`oc get issuer`
which returns
```
NAME                                         READY
<APIC mgmt deployment name>-ingress-issuer   True`
```

9. Create the analytics CR from the following template into a file called a7s.yaml
```yaml
apiVersion: analytics.apiconnect.ibm.com/v1beta1
kind: AnalyticsCluster
metadata:
  name: <Analytics Deployment name>
  namespace: <namespace on the remote analytics cluster>
spec:
  appVersion: 10.0.0.0
  certManagerIssuer:
    kind: Issuer
    name: <Analytics Deployment name>-self-signed
  client:
    clientSubjectDN: 'CN=<APIC mgmt deployment name>-a7s-cl-client,O=cert-manager'
    endpoint:
      annotations:
        certmanager.k8s.io/issuer: <APIC mgmt deployment name>-ingress-issuer
      hosts:
        - name: <analytics client endpoint>
          secretName: <Analytics Deployment name>-endpoint-secret
  ingestion:
    clientSubjectDN: 'CN=<APIC mgmt deployment name>-a7s-ing-client,O=cert-manager'
    endpoint:
      annotations:
        certmanager.k8s.io/issuer: <APIC mgmt deployment name>-ingress-issuer
      hosts:
        - name: <analytics ingestion endpoint>
          secretName: <Analytics Deployment name>-ai-endpoint-secret
  license:
    accept: true
    use: nonproduction
  microServiceSecurity: certManager
  profile: n1xc2.m16
  storage:
    data:
      volumeClaimTemplate:
        storageClassName: <block storage class>
        volumeSize: 200Gi
    master:
      volumeClaimTemplate:
        storageClassName: <block storage class>
        volumeSize: 10Gi
```

10. run `oc apply -f a7s.yaml` into the remote analytics cluster
11. Wait 5 mins and have a coffee for the  pods to start
12. Log in to the APIC Cloud Admin on the management server on the original cluster and register the Analytics Client Service. Use the default TLS Profile.
