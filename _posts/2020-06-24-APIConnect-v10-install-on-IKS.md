---
layout: post
date: 2020-6-24 00:12:00
categories: APIConnect
title: "API Connect v10 - Install on IKS with IBM Entitlement Registry "
---

API Connect v10 was released on the 16 th of June 2020. This guide shows you the steps to take a vanilla IKS 1 - 17 to a fully working APIC v10.

<!--more-->
This will be a living document updated as needed. These instructions assume you have access to APIConnect v10 through the IBM Entitlement Registry  

## Part 1 - Download the files from PPA
From Passport Advantage download

`IBM API Connect Operator Install Files 1.0.0 long-term support for Containers English (CC6SWEN )`

This file is 0.5 megabytes and was published on 16th June 2020.

Once it is downloaded the zip file will be named `release_files.zip`

## Part 2 - Pre Reqs

1 - Deploy kubernetes in IKS 1.17.

2 - Confirm the cluster name

`ibmcloud cs clusters`

returns

```
OK
Name    ID           State  Created   Workers  Location  Version    Resource Group Name  Provider  
v10-k8s2  brlsmorl0vj0ige9tgp0  normal  4 days ago  3     London   1.17.6_1526  default        classic  
```
In the example above we need to make a note of `v10-k8s2`

3 - Get the kubernetes config

Run the following command `ibmcloud cs cluster config --cluster <clustername>`

e.g. `ibmcloud cs cluster config --cluster v10-k8s2`

returns

```
OK
The configuration for v10-k8s2 was downloaded successfully.

Added context for v10-k8s2 to the current kubeconfig file.
You can now execute 'kubectl' commands against your cluster. For example, run 'kubectl get nodes'.
```

4 - Initialise helm
Helm is used only for installing the block storage depenency. You must have the helm client on your laptop, this can be helm2 or helm3.

Run the following commands

```shell
helm init
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```


5 - Install IBM Block Storage Plugin

```
helm repo add iks-charts https://icr.io/helm/iks-charts
helm repo update

#helm3
helm install ibm-block-storage iks-charts/ibmcloud-block-storage-plugin -n kube-system

#helm2
helm install --name ibm-block-storage iks-charts/ibmcloud-block-storage-plugin -n kube-system
```

Check the storage classes are created.
`kubectl get storageclass`

Returns
```
NAME            PROVISIONER     RECLAIMPOLICY  VOLUMEBINDINGMODE  ALLOWVOLUMEEXPANSION  AGE
default          ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-block-bronze     ibm.io/ibmc-block  Delete     Immediate      true          3d10h
ibmc-block-custom     ibm.io/ibmc-block  Delete     Immediate      true          3d10h
ibmc-block-gold      ibm.io/ibmc-block  Delete     Immediate      true          3d10h
ibmc-block-retain-bronze  ibm.io/ibmc-block  Retain     Immediate      true          3d10h
ibmc-block-retain-custom  ibm.io/ibmc-block  Retain     Immediate      true          3d10h
ibmc-block-retain-gold   ibm.io/ibmc-block  Retain     Immediate      true          3d10h
ibmc-block-retain-silver  ibm.io/ibmc-block  Retain     Immediate      true          3d10h
ibmc-block-silver     ibm.io/ibmc-block  Delete     Immediate      true          3d10h
ibmc-file-bronze      ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-bronze-gid    ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-custom      ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-gold (default)  ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-gold-gid     ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-retain-bronze  ibm.io/ibmc-file  Retain     Immediate      false         4d
ibmc-file-retain-custom  ibm.io/ibmc-file  Retain     Immediate      false         4d
ibmc-file-retain-gold   ibm.io/ibmc-file  Retain     Immediate      false         4d
ibmc-file-retain-silver  ibm.io/ibmc-file  Retain     Immediate      false         4d
ibmc-file-silver      ibm.io/ibmc-file  Delete     Immediate      false         4d
ibmc-file-silver-gid    ibm.io/ibmc-file  Delete     Immediate      false         4d
```

6 - Install custom ingress
IKS Ingress does not support SSL Passthrough and so we must install the community Ingress.

Save this as `ingress-config.yaml`
```yaml
controller:
  config:
    hsts-max-age: "31536000"
    keepalive: "32"
    log-format: '{ "@timestamp": "$time_iso8601", "@version": "1", "clientip": "$remote_addr",
      "tag": "ingress", "remote_user": "$remote_user", "bytes": $bytes_sent, "duration":
      $request_time, "status": $status, "request": "$request_uri", "urlpath": "$uri",
      "urlquery": "$args", "method": "$request_method", "referer": "$http_referer",
      "useragent": "$http_user_agent", "software": "nginx", "version": "$nginx_version",
      "host": "$host", "upstream": "$upstream_addr", "upstream-status": "$upstream_status"
      }'
    main-snippets: load_module "modules/ngx_stream_module.so"
    proxy-body-size: "0"
    proxy-buffering: "off"
    server-name-hash-bucket-size: "128"
    server-name-hash-max-size: "1024"
    server-tokens: "False"
    ssl-ciphers: HIGH:!aNULL:!MD5
    ssl-prefer-server-ciphers: "True"
    ssl-protocols: TLSv1.2
    use-http2: "true"
    worker-connections: "10240"
    worker-cpu-affinity: auto
    worker-processes: "1"
    worker-rlimit-nofile: "65536"
    worker-shutdown-timeout: 5m
  daemonset:
    useHostPort: false
  extraArgs:
    annotations-prefix: ingress.kubernetes.io
    enable-ssl-passthrough: true
  hostNetwork: true
  kind: DaemonSet
  name: controller
rbac:
  create: "true"
```
Run to install ingresss

`helm install stable/nginx-ingress --name ingress --values ingress-config.yml --namespace kube-system`

returnss
```
NAME:   ingress
LAST DEPLOYED: Thu Jun 25 19:24:23 2020
NAMESPACE: kube-system
STATUS: DEPLOYED

RESOURCES:
==> v1/ClusterRole
NAME                   AGE
ingress-nginx-ingress  1s

==> v1/ClusterRoleBinding
NAME                   AGE
ingress-nginx-ingress  1s

==> v1/ConfigMap
NAME                              DATA  AGE
ingress-nginx-ingress-controller  18    1s

==> v1/DaemonSet
NAME                              DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR  AGE
ingress-nginx-ingress-controller  4        4        0      4           0          <none>         1s

==> v1/Deployment
NAME                                   READY  UP-TO-DATE  AVAILABLE  AGE
ingress-nginx-ingress-default-backend  0/1    1           0          1s

==> v1/Pod(related)
NAME                                                   READY  STATUS             RESTARTS  AGE
ingress-nginx-ingress-controller-62rs4                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-pvplx                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-st6jg                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-vhxrt                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-default-backend-cb576588c-j9src  0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-62rs4                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-pvplx                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-st6jg                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-controller-vhxrt                 0/1    ContainerCreating  0         1s
ingress-nginx-ingress-default-backend-cb576588c-j9src  0/1    ContainerCreating  0         1s

==> v1/Role
NAME                   AGE
ingress-nginx-ingress  1s

==> v1/RoleBinding
NAME                   AGE
ingress-nginx-ingress  1s

==> v1/Service
NAME                                   TYPE          CLUSTER-IP     EXTERNAL-IP     PORT(S)                     AGE
ingress-nginx-ingress-controller       LoadBalancer  172.21.149.42  149.81.114.237  80:30306/TCP,443:30078/TCP  1s
ingress-nginx-ingress-default-backend  ClusterIP     172.21.32.198  <none>          80/TCP                      1s

==> v1/ServiceAccount
NAME                           SECRETS  AGE
ingress-nginx-ingress          1        1s
ingress-nginx-ingress-backend  1        1s


NOTES:
The nginx-ingress controller has been installed.
It may take a few minutes for the LoadBalancer IP to be available.
You can watch the status by running 'kubectl --namespace kube-system get services -o wide -w ingress-nginx-ingress-controller'

An example Ingress that makes use of the controller:

  apiVersion: extensions/v1beta1
  kind: Ingress
  metadata:
    annotations:
      kubernetes.io/ingress.class: nginx
    name: example
    namespace: foo
  spec:
    rules:
      - host: www.example.com
        http:
          paths:
            - backend:
                serviceName: exampleService
                servicePort: 80
              path: /
    # This section is only required if TLS is to be enabled for the Ingress
    tls:
        - hosts:
            - www.example.com
          secretName: example-tls

If TLS is enabled for the Ingress, a Secret containing the certificate and key must also be provided:

  apiVersion: v1
  kind: Secret
  metadata:
    name: example-tls
    namespace: foo
  data:
    tls.crt: <base64 encoded cert>
    tls.key: <base64 encoded key>
  type: kubernetes.io/tls
```

7 - Add hostname to custom Ingress
In order to use the custom ingress with a hostname we must create a load balancer.

Run the following command to get the external IP for the community ingress. `kubectl get svc -n kube-system 	ingress-nginx-ingress-controller  `

Returns

```
NAME                TYPE      CLUSTER-IP  EXTERNAL-IP    PORT(S)           AGE
ingress-nginx-ingress-controller    LoadBalancer  152.21.5.44  159.142.219.218  80:30829/TCP,443:32422/TCP  3d7h
```

Make a note of `159.142.219.218`

Now run
```
ibmcloud ks nlb-dns create classic --cluster <clustername> --ip <external ip from above>
```

for example

```
ibmcloud ks nlb-dns create classic --cluster v10-k8s2 --ip 159.142.219.218
```

This returns something similar to the below

```
NLB hostname was created as v10-k8s2-420eb34h056ae68f3969289d61f61851-0002.eu-gb.containers.appdomain.cloud
```

Make a note of the hostname above.


8 - Install certman
Certman is an optional tool to assist with the creation of SSL certificates.

`kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.12.0/cert-manager.yaml`

## Part 3 Installing API Connect v10

1 - Create the namespace to install API Connect into.

`kubectl create ns a<namespace name>`

For Example

`kubectl create ns apic`

2 - Create ibm-entitlenment-key
In order to connect to the entitlement registry we must have a secret containing the your personal token.

2.1 - Go to [https://myibm.ibm.com/products-services/containerlibrary ](https://myibm.ibm.com/products-services/containerlibrary) and copy the key.

2.2 - Run the following command

`kubectl create secret -n <namespace> docker-registry ibm-entitlement-key --docker-server=cp.icr.io --docker-username=cp --docker-password=<your IBM Entitled registry key>`

e.g.

`kubectl create secret -n apic docker-registry ibm-entitlement-key --docker-server=cp.icr.io --docker-username=cp --docker-password=eyJhbGciOiJIUzI1NiJ9.eyNOTAREALKEYBUTITWILLBEABITLONGERTHENTHIS.0FXuM3wvlr72K-pbUODVEjk2qqL3d_vs4jPJzt8MQUQ
`

Returns

`secret/ibm-entitlement-key created`


3 - Create DataPower admin credentials
The default password for datapower must be created in a secret ahead of time.

`kubectl create secret generic datapower-admin-credentials --from-literal=password=<password> -n <namespace>`

for example.

`kubectl create secret generic datapower-admin-credentials --from-literal=password=PickABetterPasssword -n apic`


4 - Unzip release_files.zip

5 - Install the API Connect CRD

`kubectl apply -f ibm-apiconnect-crds.yaml`

Returns

```
customresourcedefinition.apiextensions.k8s.io/analyticsbackups.analytics.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/analyticsclusters.analytics.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/analyticsrestores.analytics.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/pgclusters.crunchydata.com created
customresourcedefinition.apiextensions.k8s.io/pgpolicies.crunchydata.com created
customresourcedefinition.apiextensions.k8s.io/pgreplicas.crunchydata.com created
customresourcedefinition.apiextensions.k8s.io/pgtasks.crunchydatsa.com created
customresourcedefinition.apiextensions.k8s.io/gatewayclusters.gateway.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/managementbackups.management.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/managementclusters.management.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/managementrestores.management.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/natsclusters.nats.io created
customresourcedefinition.apiextensions.k8s.io/natsserviceroles.nats.io created
customresourcedefinition.apiextensions.k8s.io/portalbackups.portal.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/portalclusters.portal.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/portalrestores.portal.apiconnect.ibm.com created
customresourcedefinition.apiextensions.k8s.io/natsstreamingclusters.streaming.nats.io created
customresourcedefinition.apiextensions.k8s.io/datapowerservices.datapower.ibm.com created
```

6 - Edit ibm-apiconnect.yaml

6.1 - Change `apic-dev-docker-local.artifactory.swg-devops.com/velox/v1000/` to `cp.icr.io/cp/`

6.2 - Change all instances of `default` to the namespace you created in Part 2.1

6.3 - Change `apic-registry-secret` to `ibm-entitlement-key`

7 - Run `kubectl apply -f ibm-apiconnect.yaml -n <namespace>`
e.g.
`kubectl apply -f ibm-apiconnect.yaml -n apic`

8 - Edit ibm-datapoweryaml

8.1 - Change `datapower-docker-local.artifactory.swg-devops.com` to `ibmcom/``

8.2 - Change all instances of default to the namespace you created

8.3 - datapower-docker-local-cred to ibm-entitlement-key

9 - Run `kubectl apply -f ibm-datapower.yaml -n <namespace>`

e.g.

`kubectl apply -f ibm-datapower.yaml -n apic`


10 - Check the pods have started with an output similar to below.

```
bash-2$ kubectl get po -napic
NAME                               READY  STATUS   RESTARTS  AGE
datapower-operator-5d88c99bfc-rvqmk                1/1   Running   0     70m
ibm-apiconnect-5f85df4c79-c92hj                  1/1   Running   0     52m
```

11 - Unzip helper_files.zip

12 - Update the CR files.
We need to update the variables in the files ending with `_cr.yaml`. To keep this simple I have provided sed commands for running these commands. I recommend they are run in bash. if you are not familiar with sed I recommend you go into each file and modify the value oon the left for the value after the second slash. Please note you will also need to replace the $ if you do this manually.

```shell
sed -i s/.ADMIN_USER_SECRET/datapower-admin-credentials/ *yaml
sed -i s/.APP_PRODUCT_VERSION/10.0.0.0/ *yaml
sed -i s/.DATA_VOLUME_SIZE/100Gi/ *yaml
sed -i s/.DOCKER_REGISTRY/cp.icr.io\/cp\/apic/ *yaml
sed -i s/.SECRET_NAME/ibm-entitlement-key/ *yaml
sed -i s/.STORAGE_CLASS/ibmc-block-gold/ *yaml
sed -I s/certManager$/custom/ *yaml
#This sets up a dev install not a full production.
sed -i s/.PROFILE/n1xc4.m16/ management_cr.yaml
sed -i s/.PROFILE/n1xc4.m8/ apigateway_cr.yaml
sed -i s/.PROFILE/n1xc4.m8/ v5cgateway_cr.yaml
sed -i s/.PROFILE/n1xc2.m8/ portal_cr.yaml
sed -i s/.PROFILE/n1xc2.m16/ analytics_cr.yaml

sed -i s/certmanager.k8s.io.*// *_cr.yaml
sed -i s/annotations:// *_cr.yaml

```

We must add the hostname. From Part 2 step 7, take the hostname and run the following command

```shell
sed -i s/.STACK_HOST/<From 2.7>/ *yaml
sed -i s/example.com/<From 2.7>/ custom-certs-external.yaml
```

for example

```shell
sed -i s/.STACK_HOST/v10-k8s2-420eb34f056ae68f3969289d61f61851-0002.eu-gb.containers.appdomain.cloud/ *yaml
```


13 - Now you are ready to install

```shell
kubectl apply -f custom-certs-external.yaml -n <namespace>
kubectl apply -f management_cr.yaml -n <namespace>
kubectl apply -f apigateway_cr.yaml -n <namespace>
kubectl apply -f v5cgateway_cr.yaml -n <namespace>
kubectl apply -f analytics_cr.yaml -n <namespace>
kubectl apply -f portal_cr.yaml -n <namespace>
```

e.g.

```shell
kubectl apply -f custom-certs-external.yaml -n apic
kubectl apply -f management_cr.yaml -n apic
kubectl apply -f apigateway_cr.yaml -n apic
kubectl apply -f v5cgateway_cr.yaml -n apic
kubectl apply -f analytics_cr.yaml -n apic
kubectl apply -f portal_cr.yaml -n apic
```


# Part 4 - Debug Failure

If the API Manager, Portal or Analytics fail to come up you need to look at the logs in the following pod
`ibm-apiconnect-5f85df4c79-c92hj`

If the Gateway fails to come up look in the following pods for errors
* `datapower-operator-5d88c99bfc-rk4f8 `
* `ibm-apiconnect-5f85df4c79-c92hj`
