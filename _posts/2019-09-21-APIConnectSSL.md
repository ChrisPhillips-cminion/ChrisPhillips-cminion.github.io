---
layout: post
date: 2019-09-21 06:00:00
categories: APIConnect
title: "Debugging SSL Connection Problems with API Connect"
image: /images/SSLtest.png
draft: true
Location: "Tunis Airport, Tunisia"
---

A common problem area is the SSL communication between the API Connect components. Often, this is due to SSL Passthrough not being correctly configured on the F5s or the ingress. In API Connect, the SSL communication between the API Manager and the other components must be terminated before the pods.

<!--more-->

The diagram below shows the most common network flow.

![](/images/SSLtest.png)


The API Manager connects to the load balancer, which routes traffic to the ingress.  The ingress then routes to the service, which routes to the pod.

### Gettiong the certificate Pod is exposing

Run the following command on the master or worker node.

```
kubectl get po -owide -n <namespace>
```

This returns all the pods including their current IPs. Find the pod to which you are trying to connect and make a note of the pod name and the IP address. Then describe the pod with

```
kubectl describe po -n <namespace> <podname>
```
<button class="collapsible" id="fulloutput">Full Output from the description command</button>

<div class="content" id="fulloutputdata" markdown="1">
```yaml

```
</div>



The output from this includes a description of the container ports in use. Normally SSL is configured to use 443 but it is worth confirming.  Look for a sample like below.

```yaml
sample: will go here
```


Now we have the pod IP and port. Run the following command to validate the SSL certificate being used.

***BAC: Don't you need to be using the shell on the same node as the pod for this to work?***

```
openssl s_client -connect <Pod IP>:<Pod Port>
```

This retruns a message similar to
<button class="collapsible" id="dataOpenssl1">Click here for the response</button>

<div class="content" id="dataOpenssl1data" markdown="1">
```
```
</div>

Look in the response for the certificate  and copy the text.

```
-----BEGIN CERTIFICATE-----
MIIC2zCCAcOgAwIBAgIEK/1OpjANBgkqhkiG9w0BAQsFADAlMSMwIQYDVQQDDBpj
aHJpc3MtbWFjYm9vay1wcm8tMi5sb2NhbDAeFw0xOTA1MjkxNjA3MDhaFw0yMDA1
MjgxNjA3MDhaMCUxIzAhBgNVBAMMGmNocmlzcy1tYWNib29rLXByby0yLmxvY2Fs
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA+6jC/ih3g6cwRRniqGie
vVY57t/T7deE4a5sh+ef+bbUm7Z8sPVdyscuKpMTiO5tpm5z8lPgsnK1oOYTHCaf
vJQQYNL8v4JMhjoMEYPOIMOtqmLWw2nNv1tpAUquvPNSfZllm2TVSunqF8SLeKrO
0MTbGtdL4XoubGmjpWgYRvZyrbxPrVShmv2RWm9meK4U12F7/r1l84OOEZbgREz6
pf9j2eKDq9pGzRg/vUWRu/PzH20qPuBkuHVIH1KUHRACH8FYVp34Wi9IrOu0KOYz
fil3fGzo+PHaYqVtaR2yasljS7wjy//AqO9s9xBNKaRCgmD7EotHxzLXznfqmC8S
DwIDAQABoxMwETAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQD5
B0ivubdugmqQVYbJebh2at3zJecGVjIBNlwDtsfbJIFMXBcZRWqlA6spaWZWNlaL
K65b56IlyDzfbiw0yNrHfc1QYJkEWl7AoTqSxXAA8Y57f6zoU+oK5A6yD3NF45+r
uX6RudTG3CBD1jD+aF8A+CZoO7G4Ce32Kh5IbrUX/WxTgikMCiIBeq5PbOhXfqGs
IQlsu9rVrg1RyYDgFyrfAQqMXS+dAt8NeueTOqEC20Ie+cTTpIoJgmxFfxOhBB4F
0P4GW0MdLGEaaKtPq+LpRlqRad2kck9XiKKrsqc8uKeXB+WPT4nYYUtcbRzrMIYh
hIOiXV9tMhyA1SvatKdA
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
