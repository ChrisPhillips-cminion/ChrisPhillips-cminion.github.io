---
layout: post
categories: IBMCloud
date: 2021-06-01 00:15:00
title: Copying Files between IBM Cloud Object Store (S3)
---
IBM Cloud Object Storage is IBMs S3 offerring.



<!--more-->
I recently came across the need to move all files from one bucket (store) to another bucket.  This script will handle it. You will need to login into ibmcloud first.

```bash
source=family-donotdelete-pr-tzkyt3qsqjdnnj
target=bucket2-chris
regionSource=us-geo
regionTarget=us-geo

list=$(ibmcloud cos objects --region $regionSource --bucket $source   --json | jq .Contents\[\].Key -r)
for i in $list ; do
  ibmcloud cos object-copy --region $regionTarget --bucket $target --key $i --copy-source $source/$i
done
```
