---
layout: post
date: 2019-11-05 00:01:00
categories: APIConnect
title: "API Connect - Additional DataPower configuration "
draft: true
---
This article explains how in API Connect 2018.4.1.8 you can persist additional configuration to DataPower.
<!--more-->

DataPower has a plethora of uses and configuration options. In order to exploit these in API Connect the configuration needs to be enabled directly in DataPower. In physical and virtual appliances this is not a problem as the state is persisted, however in Kubernetes by default state is not stored.

In order to persist additional DataPower config in Kubernetes the `DataPower cfg` file needs to be placed in the helm chart and referenced from the `APICUP`.


### Additional Configuration and Domains
1 Create or extend a file called `dp-extravaluesfile.yaml` in the `APICUP` project directory
2 Add the following lines into the file
```
datapower:
  additionalConfig:
  - domain: "<Domain Name>"
    config: "<Config File>"
```

| Domain Name | the domain name that the config file must be applied to, this can be `default`, `apiconnect` or a new domain. If the domain does not exist it is created. |
| Config File | Config file name that contains the datapower configuration. This can be extract from an existing DataPower file system in the config directory |

3 To add the extra values file to the `APICUP` config tun the following Command
`apicup subsys set <gwy> extra-values-file <path to dp-extravaluesfile.yaml>`

4 Now follow the steps in the **Deployment** section below.

### Additional Local files
1 Create or extend a file called `dp-extravaluesfile.yaml` in the `APICUP` project directory
2 Add the following lines into the file

```
datapower:
  additionalLocalTar: "<localtar>"
```

| localtar | name of the tar file to be applied |

3 To add the extra values file to the `APICUP` config run the following Command
`apicup subsys set <gwy> extra-values-file <path to dp-extravaluesfile.yaml>`

4 Now follow the steps in the deployment section below.

### Deployment
In order to apply these changes the helm chart needs to include these files, in `2018.4.1.8fp1` this is not an automatic action.

1. Run the following command to export the helm chart `apicup subsys install <gwy> --out gateway`
2. Go into the `gateway/helm` directory
3. Extract the dynamic-gateway-service tar file. `tar zxvf dynamic-gateway-service*tgz`
4. Copy the DataPower `Config File` and/or the `localtar` file referenced in the previous sections into the `./dynamic-gateway-service/` directory
5. Tar up the helm chart `tar zcvf dynamic-gateway-service*tgz dynamic-gateway-service`
6. Kick off the install referencing this directory `apicup subsys install <gwy>  --plan-dir gateway`


Now whenever DataPower restarts it will re run the DataPower config and load the local files into the local disk.
