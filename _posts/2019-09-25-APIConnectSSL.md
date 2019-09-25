---
layout: post
date: 2019-09-25 06:00:00
categories: APIConnect
title: "Debugging SSL Connection Problems"
image: /images/SSLtest.png
Location: "Tunis Airport, Tunisia"
---

A common problem area is the SSL communication between the API Connect components. Often, this is due to SSL Passthrough not being correctly configured on the F5s or the ingress. In API Connect, the SSL communication between the API Manager and the other components must be terminated before the pods.

<!--more-->

The diagram below shows the most common network flow.

![](/images/SSLtest.png)


The API Manager connects to the load balancer, which routes traffic to the ingress.  The ingress then routes to the service, which routes to the pod.

### Getting the certificate the Pod is exposing

Run the following command on the master or worker node.

```
kubectl describe po -n <namespace> <podname>
```
<button class="collapsible" id="fulloutput">Full Output from the description command</button>

<div class="content" id="fulloutputdata" markdown="1">
```yaml
Name:               apiconnect-ui-749848d745-sbdk6
Namespace:          default
Priority:           0
PriorityClassName:  <none>
Node:               apimdev1107/9.20.153.107
Start Time:         Thu, 12 Sep 2019 16:45:50 +0000
Labels:             app=apiconnect-ui
                    pod-template-hash=749848d745
                    release=apiconnect
Annotations:        apic-base-image: apiconnect/openresty
                    apic-base-image-build-tag: g.75cec4c3b973651480a337decc6d41b4b0668209.b.2018.4.1.n.48
                    architecture: x86_64
                    authoritative-source-url: registry.access.redhat.com
                    build: https://apiconnect-jenkins.swg-devops.com/job/velox/job/ui/job/2018.4.1/663/
                    build-date: 2019-09-12T00:14:49Z
                    built-at: 2019-09-11-20-04-02
                    cni.projectcalico.org/podIP: 172.16.0.15/32
                    com.redhat.build-host: cpt-1003.osbs.prod.upshift.rdu2.redhat.com
                    com.redhat.component: ubi7-container
                    com.redhat.license_terms: https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI
                    commit: 7c6dac7b95208fe4250444823c5890a31962a138
                    description: IBM API Connect Management ui
                    distribution-scope: public
                    git-desc: 2018.4.1-0-g7c6dac7
                    io.k8s.description: IBM API Connect Management ui
                    io.k8s.display-name: IBM API Connect Management ui
                    io.openshift.tags: apiconnect-ui
                    name: apiconnect/ui
                    productChargedContainers: All
                    productID: 460234cbf38040dbbe796bbbf79d9820
                    productMetric: PROCESSOR_VALUE_UNIT
                    productName: API Manager
                    productVersion: 2018.4.1.7
                    release: 663
                    summary: IBM API Connect Management ui
                    upstream: https://apiconnect-jenkins.swg-devops.com/job/velox/job/ui/job/2018.4.1/663/
                    url: https://access.redhat.com/containers/#/registry.access.redhat.com/ubi7/images/7.6-239
                    vcs-ref: 7c6dac7b95208fe4250444823c5890a31962a138
                    vcs-type: git
                    vendor: IBM
                    version: 1.0
Status:             Running
IP:                 172.16.0.15
Controlled By:      ReplicaSet/apiconnect-ui-749848d745
Containers:
  ui:
    Container ID:   docker://a5fbe8df17d47bc041bb6971b194cdb49b8b3d9a349c1a72018e32c2ec4789e0
    Image:          apiconnect/ui:2018.4.1-663-7c6dac7b95208fe4250444823c5890a31962a138
    Image ID:       docker://sha256:af1a38cd6dee2fc43d3899b47043c7b224b18d7c012ff6322fea030b1599adef
    Port:           8443/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 12 Sep 2019 16:45:55 +0000
    Ready:          True
    Restart Count:  0
    Requests:
      cpu:        100m
      memory:     8Mi
    Liveness:     tcp-socket :8443 delay=60s timeout=1s period=10s #success=1 #failure=3
    Readiness:    tcp-socket :8443 delay=10s timeout=1s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /etc/nginx/certs from certs-volume (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from apiconnect-ui-token-xmvcl (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  certs-volume:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  ui-velox-certs-f23b922b16f7108d0b4e9830e30794e3
    Optional:    false
  apiconnect-ui-token-xmvcl:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  apiconnect-ui-token-xmvcl
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:          <none>

```
</div>



The output from this includes a description of the container ports in use. We need to extract the Pod IP and the Port from the description. I have highlighted the key keys in the sample below.

```yaml
...
IP:  172.16.0.15
...
Containers:
  ui:
    ...
    Port:           8443/TCP
```


Now we have the pod IP and port. Run the following command to validate the SSL certificate being used.



```
openssl s_client -connect <Pod IP>:<Pod Port>
```

This retruns a message similar to
<button class="collapsible" id="dataOpenssl1">Click here for the response</button>

<div class="content" id="dataOpenssl1data" markdown="1">
```
CONNECTED(00000003)
depth=0 CN = service-server
verify error:num=20:unable to get local issuer certificate
verify return:1
depth=0 CN = service-server
verify error:num=21:unable to verify the first certificate
verify return:1
---
Certificate chain
 0 s:/CN=service-server
   i:/CN=mgmt-ca
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDZjCCAk6gAwIBAgIQXUYyLnsw0KO/pwj/262ZSDANBgkqhkiG9w0BAQsFADAS
MRAwDgYDVQQDEwdtZ210LWNhMB4XDTE5MDkxMjE2Mjk0NloXDTM5MDkwNzE2Mjk0
NlowGTEXMBUGA1UEAxMOc2VydmljZS1zZXJ2ZXIwggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQC5fR+7IZ8S6Gutk/aroFgMhr5xnmz8wWnaHKtCS3vNsAkM
InRRcOCq0j5SfK2xdBRLx3aPDfu7k8fDdqy5Gd0GLCkMN2XFD+F2xPbeXp8mWT8j
FQ6oD1sZ43vX3YWwAifuiwi2J3Ar19FeUD9WljD3eTMFLtOQMuQmAxyGBTZPjI9f
GoWLv/sRYE964WmgF6c5TB43zn2IxClBUOumT1h3AeA42zv1BQ0VSMr+rnZRz1ma
24JJdU0Qeq3tZa+rbYut7JR/OqIRJYOwD+oNu+X3PFA95dITvtTC3QwXolw4mr3m
wqHLlqsbVGuDTPEMzMoRhSeiHdKSpyPSeoAS2TUtAgMBAZGjgbAwga0wDgYDVR0P
AQH/BAQDAgWgMBMGA1UdJQQMMAoGCCsGAQUFBwMBMAwGA1UdEwEB/wQCMAAwGQYD
VR0OBBIEEE7CfrAyIMNDLNMk+XOFNW0wGwYDVR0jBBQwEoAQyYxGMEoPX4KHPIPd
wVbWjDBABgNVHREEOTA3ggkqLmRlZmF1bHSCDSouZGVmYXVsdC5zdmOCGyouZGVm
YXVsdC5zdmMuY2x1c3Rlci5sb2NhbDANBgkqhkiG9w0BAQsFAAOCAQEALFiAKJ4R
cWugHuogs3z32eEl0iPDT8vnU7joPDnbEcEGPeQsxszglyOZqLjRosAGm02FJtFJ
F89Dg1wXBgyvTk6g8B94HRXpBqLydGritAiT9vty0GV7tGEwyMa2dC8WLYd9Cfpg
eEvokQZjdCxIQaRM3xtT2hKq7rjLfR3me6LAPrVUkeQM0ddfTUMZHTKDt5yrgNXn
BDm7REd/QTifMngUnVBac+Dd2LiSviZGPiLc110EYndCjBY4l517Q6RDuwD23Ucv
SvWPz8izW5Nc4nh0Y4STbjtZsHHo0e8a7Ndw8at4TdnrSLsWg3HY7trYC81C+NjB
1P3JoDfyNDim/Q==
-----END CERTIFICATE-----
subject=/CN=service-server
issuer=/CN=mgmt-ca
---
No client certificate CA names sent
Peer signing digest: SHA512
Server Temp Key: ECDH, P-256, 256 bits
---
SSL handshake has read 1544 bytes and written 431 bytes
---
New, TLSv1/SSLv3, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 2048 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: 669D3D0985E4A77D9F9828CF0D6ECE005C2B43AB4C06E2A4AC4D46B57CD047C4
    Session-ID-ctx:
    Master-Key: A2972FB2CC2BA71190A4ACF584C26608EF3936328D0B8086BA36F464EA224A9D3436540E8EF0BFDD1D58DE6422817229
    Key-Arg   : None
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 300 (seconds)
    TLS session ticket:
    0000 - ed 17 a9 ae d5 7f 6b 2d-70 99 eb 21 01 46 2b f3   ......k-p..!.F+.
    0010 - 0b e7 68 6e cd c0 83 d6-b3 03 42 d3 0b 9c ac 0c   ..hn......B.....
    0020 - 3a 4e 82 b2 35 c1 ac c6-f3 eb 53 eb 4d c2 ba 42   :N..5.....S.M..B
    0030 - 97 62 68 31 11 16 c6 df-e9 9f ea d6 42 d6 fb 6f   .bh1........B..o
    0040 - 6b 08 5a 66 f6 55 38 6f-07 fa 46 48 b8 90 38 24   k.Zf.U8o..FH..8$
    0050 - 51 00 ce bc 43 f1 bc 8f-3f 3c ce 36 97 d7 26 cc   Q...C...?<.6..&.
    0060 - 21 68 8d 79 7b 2c 70 1a-48 d0 8a 3f a4 7c bf 7e   !h.y{,p.H..?.|.~
    0070 - 04 94 de 72 2f 17 c8 4b-30 84 e1 02 7d 3f ed 00   ...r/..K0...}?..
    0080 - 05 54 a4 02 16 32 e6 22-e2 63 40 67 5f 3c 38 98   .T...2.".c@g_<8.
    0090 - 08 a3 2b cb b7 e7 87 68-8b fe 08 bb 2a 73 05 c2   ..+....h....*s..
    00a0 - 1d cf fd 48 3e 91 cc 1f-33 3b 7e 76 cf 3e d0 cd   ...H>...3;~v.>..

    Start Time: 1569406765
    Timeout   : 300 (sec)
    Verify return code: 21 (unable to verify the first certificate)
---
^C
```
</div>

Look in the response for the certificate  and copy the text.

```
-----BEGIN CERTIFICATE-----
MIIDZjCCAk6gAwIBAgIQXUYyLnsw0KO/pwj/262ZSDANBgkqhkiG9w0BAQsFADAS
MRAwDgYDVQQDEwdtZ210LWNhMB4XDTE5MDkxMjE2Mjk0NloXDTM5MDkwNzE2Mjk0
NlowGTEXMBUGA1UEAxMOc2VydmljZS1zZXJ2ZXIwggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQC5fR+7IZ8S6Gutk/aroFgMhr5xnmz8wWnaHKtCS3vNsAkM
InRRcOCq0j5SfK2xdBRLx3aPDfu7k8fDdqy5Gd0GLCkMN2XFD+F2xPbeXp8mWT8j
FQ6oD1sZ43vX3YWwAifuiwi2J3Ar19FeUD9WljD3eTMFLtOQMuQmAxyGBTZPjI9f
GoWLv/sRYE964WmgF6c5TB43zn2IxClBUOumT1h3AeA42zv1BQ0VSMr+rnZRz1ma
24JJdU0Qeq3tZa+rbYut7JR/OqIRJYOwD+oNu+X3PFA95dITvtTC3QwXolw4mr3m
wqHLlqsbVGuDTPEMzMoRhSeiHdKSpyPSeoAS2TUtAgMBAZGjgbAwga0wDgYDVR0P
AQH/BAQDAgWgMBMGA1UdJQQMMAoGCCsGAQUFBwMBMAwGA1UdEwEB/wQCMAAwGQYD
VR0OBBIEEE7CfrAyIMNDLNMk+XOFNW0wGwYDVR0jBBQwEoAQyYxGMEoPX4KHPIPd
wVbWjDBABgNVHREEOTA3ggkqLmRlZmF1bHSCDSouZGVmYXVsdC5zdmOCGyouZGVm
YXVsdC5zdmMuY2x1c3Rlci5sb2NhbDANBgkqhkiG9w0BAQsFAAOCAQEALFiAKJ4R
cWugHuogs3z32eEl0iPDT8vnU7joPDnbEcEGPeQsxszglyOZqLjRosAGm02FJtFJ
F89Dg1wXBgyvTk6g8B94HRXpBqLydGritAiT9vty0GV7tGEwyMa2dC8WLYd9Cfpg
eEvokQZjdCxIQaRM3xtT2hKq7rjLfR3me6LAPrVUkeQM0ddfTUMZHTKDt5yrgNXn
BDm7REd/QTifMngUnVBac+Dd2LiSviZGPiLc110EYndCjBY4l517Q6RDuwD23Ucv
SvWPz8izW5Nc4nh0Y4STbjtZsHHo0e8a7Ndw8at4TdnrSLsWg3HY7trYC81C+NjB
1P3JoDfyNDim/Q==
-----END CERTIFICATE-----
```

The certificate should be the same for all the layers of the flow. Compare this certificate to what is provided in the other layers.


### Getting the certificate from the Load Balancer.

Run the following command
```
openssl s_client -connect <Public Hostname>:<Public Port>
```

Validate the certificate value matches the certificate obtained from the pod. If it does not, then the SSL connection is being terminated by one of the layers between the load balancer and the pod.

### Getting the certificate from Ingress.

Now run the following command to validate the connection to ingress.
```
openssl s_client -connect <Kuberenetes Worker Node Hostname>:<443>
```

Validate that the certificate matches the certificate obtained from the pod. If does, then the SSL is being terminated in the F5. If not then the SSL Connection is being terminated probably by Ingress itself. To confirm if ingress is the problem we run the openssl command against the service.

### Getting the certificate from the Kubernetes Service

Run the following command.
```
kubectl get service -n <namespace>
```

Then select the relevant service and make a note of the internal IP address and port. From the Kubernetes master or worker node run the following command:

```
openssl s_client -connect <Service IP>:<Service Port>
```

The certificate must match the certificate of the pod because it does not have its own certificate. If it does not then the service is connecting to the wrong pod or the pods in the same deployment are implemented badly and exposing different certificates.  If the certificate of the service does match that of the pod, but not that of the ingress then SSL is being terminated in the ingress.
