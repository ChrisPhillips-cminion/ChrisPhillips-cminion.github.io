---
layout: post
date: 2018-09-27  00:00:00
categories: APIConnect
title: 'API Connect 2018 CLI --- Login --- realm'
---
# API Connect 2018 CLI --- Login --- realm

![](https://cdn-images-1.medium.com/max/800/1*RpK5B2rBTfCGX15_7Ln6zw.png)

API Connect 2018 comes with a much better CLI then version v5. The
interface is similar but its easier to install and much quicker to run.







------------------------------------------------------------------------




However, one of the biggest stumbling blocks is that when you log in you
need to specify a realm

**TLDR**: Use the following command

`apic login -s <server> -u <username> -p <password> --realm provider/default-idp-2`

**Long Version**

The realm tells the api manager whether you want to log into the
`admin` (Cloud Manager) or
`provider` (APIM Manager) and which user
registry to use.

To get a list of realms you can run the following command, you do not
need to log in first.

`apic realms -s <server> --scope [provder|admin]`

Note: you need to specify if it is a provider or the admin you are
trying to access

You can construct the realm string for the login command using

`[provider|admin]/<realm>`





By [Chris Phillips](https://medium.com/@cminion) on
[September 27, 2018](https://medium.com/p/39f24178bf99).

[Canonical
link](https://medium.com/@cminion/api-connect-2018-cli-login-realm-39f24178bf99)

Exported from [Medium](https://medium.com) on April 6, 2019.
