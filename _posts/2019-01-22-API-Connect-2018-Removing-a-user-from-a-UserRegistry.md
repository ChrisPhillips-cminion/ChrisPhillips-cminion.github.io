---
layout: post
date: 2019-01-22  00:00:00
categories: APIConnect
title: 'API Connect 2018 ---  Removing a user from a UserRegistry'
---

API Connect 2018 ---  Removing a user from a UserRegistry
=========================================================


In API Connect you can create your own user registries, these can be
backed on to LDAP or be a local user registry.






------------------------------------------------------------------------




### API Connect 2018 --- Removing a user from a UserRegistry

In API Connect you can create your own user registries, these can be
backed on to LDAP or be a local user registry.

There are two ways to delete users from a user registry. Both of these
require that the user is no longer a member to any provider orgs. There
is no way to remove a user from a user registry in the UI today.

1.  [Delete yourself with the CLI]

Login as the user you wish to delete

```
apic login -s <Platform API endpoint> -u <username> --realm <provider|admin>/<user repository>
```

run the following command

```
apic me:delete -s <Platform API endpoint>
```

e.g.

```
apic me:delete -s platform.cminion.cf
```

2\. Delete someone else using the CLI

Login as an admin to the API Cloud to the admin realm

```
apic login -s <Platform API endpoint> -u <username> --realm admin/<user repository>
```

e.g.

```
apic login —u admin -s platform.cminion.cf  --realm admin/default-idp-1
```

List the users. **Please Note: the organisation must be set to admin.**

```
apic users:list -o admin -s <Platform API endpoint> --user-registry <User registry you wish to remove the user from>
```

e.g.

```
apic users:list -o admin -s platform.cminion.cf --user-registry test-ldap
```

This returns

```
hamster                                https://platform.cminion.cf/api/user-registries/4a1d6fb2-3c81-493e-b168-f76fce33cf37/ef389d90-875b-43dd-988e-2487301d2991/users/ac120227-68ce-49e2-be87-634ac70a7ec2
```

```
jo                                     https://platform.cminion.cf/api/user-registries/4a1d6fb2-3c81-493e-b168-f76fce33cf37/ef389d90-875b-43dd-988e-2487301d2991/users/fdf0bb82-104b-4576-b988-811a820a188b
```

```
rainbowjess11                          https://platform.cminion.cf/api/user-registries/4a1d6fb2-3c81-493e-b168-f76fce33cf37/ef389d90-875b-43dd-988e-2487301d2991/users/1bd06598-4007-4b8c-9417-d790f3df8294
```

```
val                                    https://platform.cminion.cf/api/user-registries/4a1d6fb2-3c81-493e-b168-f76fce33cf37/ef389d90-875b-43dd-988e-2487301d2991/users/b9bdb3fa-d285-4906-b8a2-a09ccd68069c
```

Take the GUID for the user which is the string after the last /

e.g. for jo it is `fdf0bb82–104b-4576-b988–811a820a188b`

Run the following command

```
apic users:delete <guid> -o admin -s <Platform API endpoint> --user-registry <User registry you wish to remove the user from>
```

e.g.

```
apic users:delete fdf0bb82–104b-4576-b988–811a820a188b -o admin -s platform.cminion.cf --user-registry test-ldap
```





By [Chris Phillips](https://medium.com/@cminion) on
[January 22, 2019](https://medium.com/p/3320a4728de5).

[Canonical
link](https://medium.com/@cminion/api-connect-2018-removing-a-user-from-a-userregistry-3320a4728de5)

Exported from [Medium](https://medium.com) on April 6, 2019.
