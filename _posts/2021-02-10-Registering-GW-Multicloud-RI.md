---
layout: post
categories: APIConnect
date: 2021-02-08 00:14:00
title: Configuring a Gateway in a different cloud - tips for RI
---

Following up from my previous article these are the considerations you need to make when working with the Reserved Instance.
<!--more-->

1. Getting the CA to load into datapower. This is used with step

`curl -o - http://apps.identrust.com/roots/dstrootcax3.p7c 2> /dev/null | openssl pkcs7 -inform DER -print_certs`

The URL is discovered from inside certificates exposed on the API manager. With this command openssl

`openssl s_client -connect  <apimanager api endpoint>:443 -servername <apimanager api endpoint> -showcerts`


2. For step 7 you need to load the certificates into a certificate manager in IBM Cloud - This is documented here.
https://www.ibm.com/support/knowledgecenter/en/SSMNED_v10cloud/com.ibm.apic.install.doc/ri_gwy_certs_auth_svc.html

**For Reference**
Management -> CA Bundles is loaded into CMC as a TrustStore
Management -> Certificate loaded into CMC as a KeyStore
When you specify the Certificate it loads the Key into the KeyStore, when you specify the CA bundle it loads the cert into the Trust store
When the TLS Client Profile is created it points to the Key Store and the Trust Store above to use to communicate with the gateway
