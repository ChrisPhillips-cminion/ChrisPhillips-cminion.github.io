---
layout: post
date: 2020-6-24 00:12:00
categories: APIConnect
title: "API Connect v10 - Install on IKS with IBM Entitlement Registry "
---

API Connect v10 was released on the 16 th of June 2020. This guide shows you the steps to take a vanilla IKS 1 - 17 to a fully working APIC v10.

<!--more-->
This will be a living document updated as needed. These instructions assume you have access to APIConnect v10 through the IBM Entitlement Registry  

## Part 1 - - Download the files from PPA
From Passport Advantage download

`IBM API Connect Operator Install Files 1 - .0.0 long-term support for Containers English (CC6SWEN )`

This file is 0.5 megabytes and was published on 1 - th June 2020.

Once it is downloaded the zip file will be named `release_files.zip`

## Part 2 - Pre Reqs

1 - Deploy kubernetes in IKS 1 - 17.

2 - Confirm the cluster name

`ibmcloud cs clusters`

returns

```
OK
Name    ID           State  Created   Workers  Location  Version    Resource Group Name  Provider  
v10-k8s2  brlsmorl0vj0ige9tgp0  normal  4 days ago  3     London   1 - 17.6_1526  default        classic  
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
IKS Ingress does not support SSL Passthrough and so we must install the community Ingress. v0.30 is the recommend version

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/mandatory.yaml
```

Returns

```
namespace/ingress-nginx created
configmap/nginx-configuration created
configmap/tcp-services created
configmap/udp-services created
serviceaccount/nginx-ingress-serviceaccount created
clusterrole.rbac.authorization.k8s.io/nginx-ingress-clusterrole created
role.rbac.authorization.k8s.io/nginx-ingress-role created
rolebinding.rbac.authorization.k8s.io/nginx-ingress-role-nisa-binding created
clusterrolebinding.rbac.authorization.k8s.io/nginx-ingress-clusterrole-nisa-binding created
deployment.apps/nginx-ingress-controller created
limitrange/ingress-nginx created
```

6.2 - Save the following yaml file and run it.

*ingress-svc.yaml*
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx
spec:
  type: LoadBalancer
  selector:
    app: ingress-nginx
  ports:
   - name: http
     protocol: TCP
     port: 80
   - name: https
     protocol: TCP
     port: 443
  externalTrafficPolicy: Cluster
```

run

```
kubectl apply -n ingress-nginx -f  ingrees-svc.yaml

```

7 - Add hostname to custom Ingress
In order to use the custom ingress with a hostname we must create a load balancer.

Run the following command to get the external IP for the community ingress. `kubectl get svc -n ingress-nginx 	ingress-nginx`

Returns

```
NAME                TYPE      CLUSTER-IP  EXTERNAL-IP    PORT(S)           AGE
ingress-nginx-ingress  LoadBalancer  1 - 2.21.5.44  1 - 9.142.219.218  80:30829/TCP,443:32422/TCP  3d7h
```

Make a note of `159.142.219.218`

Now run
```
ibmcloud ks nlb-dns create classic --cluster <clustername> --ip <external ip from above>
```

for example

```
ibmcloud ks nlb-dns create classic --cluster v10-k8s2 --ip 1 - 9.142.219.218
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
bash- 3 - 2$ kubectl get po -napic
NAME                               READY  STATUS   RESTARTS  AGE
datapower-operator-5d88c99bfc-rvqmk                1 - 1   Running   0     70m
ibm-apiconnect-5f85df4c79-c92hj                  1 - 1   Running   0     52m
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
