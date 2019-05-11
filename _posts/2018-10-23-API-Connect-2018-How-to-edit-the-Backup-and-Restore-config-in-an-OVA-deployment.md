---
layout: post
date: 2018-10-23  00:00:00
categories: APIConnect
title: |
    API Connect 2018 --- How to edit the Backup and Restore config in an OVA
    deployment
---

API Connect 2018 --- How to edit the Backup and Restore config in an OVA deployment
===================================================================================


Recently we got asked how do we enable back up of the API Manager in an
API Connect OVA deployment that is already running.






------------------------------------------------------------------------




### API Connect 2018 --- How to edit the Backup and Restore config in an OVA deployment

Recently we got asked how do we enable back up of the API Manager in an
API Connect OVA deployment that is already running.

[Rob Thelen](https://medium.com/u/e3752a478e37) acquired the following steps.

1.  [SSH into an API Management OVA]
2.  [Run the following command to become root `sudo su -`]
3.  [Run `kubectl get cc` to get the
    name of the API Connect CC object]
4.  [Run `kubectl edit cc <name> `e.g
    `kubectl edit cc r264f70e7bf-apiconnect-cc`]
5.  [Modify the spec.backup section so it is similar to below]

```
spec:
  backup:
    args:
      host: <SFTP_HOST>
      path: <DEST_PATH>
      port: <SFTP PORT>
      protocol: sftp
      retries: 5
      secretName: sftp-user-pass
      schedule: ""
```

e.g.

```
spec:
  backup:
    args:
      host: cminio.cf
      path: /backup
      port: 22
      protocol: sftp
      retries: 5
      secretName: cassandra-backup-auth-secret-6f2d51587cf14798c0f18e7b7ea07594
      schedule: ""
```

6\. If the secret does not exist for the ftp user then run the following
command

`kubectl create secret generic sftp-user-pass — from-file=./username — from-file=./password -n <KUBE_NAMESPACE>`

7\. Run the following command on your local system to complete a backup
`apic backup create`





By [Chris Phillips](https://medium.com/@cminion) on
[October 23, 2018](https://medium.com/p/db9c88fe2dad).

[Canonical
link](https://medium.com/@cminion/api-connect-2018-how-to-edit-the-backup-and-restore-config-in-an-ova-deployment-db9c88fe2dad)

Exported from [Medium](https://medium.com) on April 6, 2019.
