---
layout: post
date: 2018-12-20  00:00:00
categories: APIConnect
title: OpenLDAP with Samba
---

OpenLDAP with Samba
===================


So like all good techies I have spent my week off setting up my home
LDAP because I need to ensure my kids (8 and 6) need to learn about...






------------------------------------------------------------------------




### OpenLDAP with Samba

So like all good techies I have spent my week off setting up my home
LDAP because I need to ensure my kids (8 and 6) need to learn about
enterprise computing.

OpenLDAP is an Open Source User Registry. Samba is a file sharing system
that allows you to share files across a network. The aim here is to
allow users to log into the samba service with users from the LDAP.

LDAP in K8s was a dream. Backing samba (not running in k8s) on to the
LDAP was a challenge.

This articles assumes you have a working samba not using LDAP and a
working LDAP.

Add the following config to the `/etc/samba/smb.conf`

```
[global]
```

```
WORKGROUP=WORKGROUP
```

```
passdb backend = ldapsam:ldap://192.168.1.132
```

```
ldap suffix = dc=cminion,dc=cf
```

```
ldap admin dn = cn=admin,dc=cminion,dc=cf
```

```
ldap ssl = no
```

```
ldap passwd sync = yes
```

Once you have done this you need to run the following to configure the
password for the admin user.

`smbpasswd -w <Password for the admin dn>`

then cycle the SMB service and you should be good to go

`sudo service smbd restart`





By [Chris Phillips](https://medium.com/@cminion) on
[December 20, 2018](https://medium.com/p/bd929f93401a).

[Canonical
link](https://medium.com/@cminion/openldap-with-samba-bd929f93401a)

Exported from [Medium](https://medium.com) on April 6, 2019.
