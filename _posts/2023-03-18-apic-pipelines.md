---
layout: post
date: 2023-03-18 00:01:00
categories: APIConnect
title: "OpenShift Pipeline - Publish APIC"
draft: true
---

I have been asked almost daily for the last few weeks what is my preferred CIDC took or process.  My answer is always the same, given APIC has a rest interface the best tool is the one the team know.

<!--more-->

However, this is not often seen as an acceptable answer. I decided to dive back into OCP Pipelines. I set myself two hours to see what I could put together. This is by no means perfect but will meet the initial needs.  

**Requirements**
1. OpenShift Environment - I did this with OCP 4.10
2. OpenShift Pipelines Operator installed

![https://chrisphillips-cminion.github.io/images/ocppipelines.png](https://chrisphillips-cminion.github.io/images/ocppipelines.png)

**My Task**

I have placed my task on github here [https://gist.github.com/ChrisPhillips-cminion/ea228d9ea3429bad11ad0a1c30f48b59](https://gist.github.com/ChrisPhillips-cminion/ea228d9ea3429bad11ad0a1c30f48b59)

Save the gist to a local file and load it with

`oc apply -f ./apic-publish-task.yaml`

This must be loaded into the namespace that will host the pipeline.

**Script in the task**

The task linked above contains the following script that requires passes in the listed variables. This script can be seen as a starting point for any customisations required.

| Environmental Variables |  Description |
|  ---- |  ---- |
| dir | The subdirectory to look for products in |
| url | The API Manager URL|
| user | The user to log into api manager |
| password | The password to log into api manager |
| realm | The user registry |
| target_porg | The Provider Org to publish the product to |
| target_catalog | The Catalog to publish the product to |
| target_space | The Space to publish the product to |
| replace_subscriptions | Automatically migrate subscriptions to the new product if it is replacing a product of the same name and version |


```shell
#!/bin/sh
if [ "replace_subscriptions" == "" ] ; then #Set the migrate subscriptions flag, or not
  migrate_subscriptions=""
else
  migrate_subscriptions="--migrate_subscriptions"
fi
if [ "$target_space" == "" ] ; then #If spaces are used set the scope to space
  scope="space"
else
  scope="catalog"
fi
rm -rf toolkit* #Clean up
echo Downloading CLI tool #Download the CLI from the API Manager, As the API manager must be assessable to publish APIs there should be near zero risk that it will not be contactable.  
curl https://$url/client-downloads/toolkit-linux.tgz -k -o toolkit-linux.tgz
tar zxvf toolkit-linux.tgz
chmod 755 apic-slim
echo Login #to api manager
./apic-slim --accept-license login -s $url --realm $realm --username $user --password $password
product_list=$(grep -ri product:\ 1.0.0 $dir | sed -e s/:.\*//) #Get the product files from the git repo.
echo Publishing to $publish_url
for i in $product_list ; do
  echo "publishing ./apic-slim products:publish $i -s $url -o $target_porg -c $target_catalog --scope $scope $migrate_subscriptions"
  ./apic-slim products:publish $i -s $url -o $target_porg -c $target_catalog --scope $scope $migrate_subscriptions
done
```

**Create the Pipeline**

![https://chrisphillips-cminion.github.io/images/pipeline.png](https://chrisphillips-cminion.github.io/images/pipeline.png)

I wont repeat a thousand other articles on how to create a pipeline, but I will provide a sample here.
[https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb](https://gist.github.com/ChrisPhillips-cminion/830ac19b20e6985a31e9e6ce7e13eceb)

This simple pipeline will extract from git and then publish the products listed.
