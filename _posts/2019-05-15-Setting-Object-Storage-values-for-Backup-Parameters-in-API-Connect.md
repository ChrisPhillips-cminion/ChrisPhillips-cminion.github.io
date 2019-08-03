---
layout: post
date: 2019-05-15  00:00:00
categories: APIConnect
title: 'Setting Object Storage values for Backup Parameters in API Connect 2018.4.1.X [Guest Post by Nick Cawood]'
author: ["NickCawood"]
---


In a Container Service like IKS Object Storage can be selected as the back storage destination for the Management and Portal subsystems. Knowledge Center contains guidance for the parameters for the backups (set with apicup tool) but for clarity here is some guidance on how these translate to the values you need to extract from your Container Service and use.

<!--more-->

| Component | Parameter | Description|
|-------|------------|------------|
| Management | cassandra-backup-host | The private endpoint for the Bucket / region (e.g. s3.private.eu-de.cloud-object-storage.appdomain.cloud/eu-de). |
| Management | cassandra-backup-path | The "Bucket Name" from your Container Service Object Storage. |
| Management | cassandra-backup-auth-user | The username of the Service Account in the Container Service. |
| Management | cassandra-backup-auth-pass | The password of the Service Account in the Container Service (apicup --validate will encrypt this value).
| Management | cassandra-backup-protocol | The Backup Protocol e.g. `ObjStore` |
| Management | cassandra-backup-schedule | The cronjob backup schedule e.g. `"0 0 * * *"`|
|Portal | site-backup-host |  The private endpoint for the Bucket / region (e.g. s3.private.eu-de.cloud-object-storage.appdomain.cloud/eu-de). |
| Portal | site-backup-path | The "Bucket Name" from your Container Service Object Storage.|
| Portal | site-backup-auth-user |  The username of the Service Account in the Container Service. |
| Portal | site-backup-auth-pass |  The password of the Service Account in the Container Service (apicup --validate will encrypt this value). |
| Portal | site-backup-protocol | The Backup Protocol e.g. `ObjStore` |
| Portal | site-backup-schedule | The cronjob backup schedule e.g. `"0 0 * * *"`|


These parameters are set / re-set with the apicup apicup subsys set management portal commands and then instantiated with the apicup subsys install management portal command.
