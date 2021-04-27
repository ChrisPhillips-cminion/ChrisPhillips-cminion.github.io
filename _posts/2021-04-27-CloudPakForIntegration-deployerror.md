---
layout: post
categories: CP4I
date: 2021-04-27 00:15:00
title: Cloud Pak for Integration fails to deploy the platform navigator

---

When customers deploy CP4I Platform Navigator for CP4I 2021.1 in ROKS it is not uncommon to see the following situation.

```
NAME                          READY   STATUS             RESTARTS   AGE
create-secrets-job-qfh6h      0/1     Completed          0          9h
zen-metastoredb-0             0/1     CrashLoopBackOff   116        9h
zen-metastoredb-1             0/1     CrashLoopBackOff   116        9h
zen-metastoredb-2             0/1     CrashLoopBackOff   116        9h
zen-metastoredb-certs-m7gf4   0/1     Completed          0          9h
zen-metastoredb-init-jv4nq    1/1     Running            0          9h
```


<!--more-->

When you look into the logs of the `zen-metastoredb-0`  you see the following

```
$ oc logs zen-metastoredb-0
++ hostname
+ exec /cockroach/cockroach start --max-offset=1000ms --temp-dir=/tmp --max-disk-temp-storage 8GiB --logtostderr --certs-dir=/certs --advertise-host zen-metastoredb-0.zen-metastoredb --http-host 0.0.0.0 --http-port 8080 --port 26257 --cache 25% --max-sql-memory 25% --join zen-metastoredb-0.zen-metastoredb:26257,zen-metastoredb-1.zen-metastoredb:26257,zen-metastoredb-2.zen-metastoredb:26257
E210427 21:13:31.997512 1 cli/error.go:233  unable to create log directory: mkdir /cockroach/cockroach-data/logs: permission denied
Error: unable to create log directory: mkdir /cockroach/cockroach-data/logs: permission denied
Failed running "start"
```

In ROKS this is because the storage class being used is `ibmc-file-gold` where it should be `ibmc-file-gold-gid`.
