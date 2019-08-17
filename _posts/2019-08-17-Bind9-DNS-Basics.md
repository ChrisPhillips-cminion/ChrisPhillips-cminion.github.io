---
layout: post
date: 2019-08-17 07:00:00
categories: misc
title: "Bind9 DNS Basics"
---

Today I sat down and installed Bind9 to act as a local DNS server. As this took me far to long I have attached a config similar to my home one explaining the changes I made from the default.

<!--more-->


**/etc/named.config**

```
acl goodclients {
    localhost;
    192.168.0.0/24;
};
```
Crate a list of clients who are allowed to access the dns server. This is to avoid the DNS server being used for DDOS attacks.  `192.168.0.0/24` says accept all requests from `192.168.x.x`. I have changed IP ranges for this article.

```
listen-on port 53 { 127.0.0.1; 192.168.0.200; };
```
Enter the IP of the DNS server

```
forwarders {
        8.8.8.8;
        8.8.4.4;
};
```
In order to look up public IP addresses a public DNS Provider must be configured.

```
include "/etc/named/named.conf.local";
```
Continue the config in the specified file

<button class="collapsible" id="yaml">Click here for the complete /etc/named.conf.</button>
<div class="content" id="yamldata" markdown="1">
```
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//
// See the BIND Administrator's Reference Manual (ARM) for details about the
// configuration located in /usr/share/doc/bind-{version}/Bv9ARM.html
acl goodclients {
    localhost;
    192.168.0.0/24;
};

options {
	listen-on port 53 { 127.0.0.1; 192.168.0.200; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	recursing-file  "/var/named/data/named.recursing";
	secroots-file   "/var/named/data/named.secroots";
	allow-query     { goodclients; };
	recursion yes;
  forwarders {
          8.8.8.8;
          8.8.4.4;
  };
	dnssec-enable yes;
	dnssec-validation yes;

	/* Path to ISC DLV key */
	bindkeys-file "/etc/named.iscdlv.key";

	managed-keys-directory "/var/named/dynamic";

	pid-file "/run/named/named.pid";
	session-keyfile "/run/named/session.key";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
include "/etc/named/named.conf.local";

```
</div>

**/etc/named/named.conf.local**
```
zone "myhome.cf" {
    type master;
    file "/etc/named/zones/dns.myhome.cf"; # zone file path
};
```
Configure the zone for look ups, the directory is stored in `/etc/named/zones/dns.myhome.cf`

```
zone "192.in-addr.arpa" {
    type master;
    file "/etc/named/zones/db.192";  # 192.0.0.0/8  subnet
};
```
Configure the zone for the reverse look ups, the director is stored in /etc/named/zones/db.192


<button class="collapsible" id="yaml2">Click here for the complete /etc/named/named.conf.local.</button>
<div class="content" id="yaml2data" markdown="1">
```
zone "myhome.cf" {
    type master;
    file "/etc/named/zones/dns.myhome.cf"; # zone file path
};

zone "192.in-addr.arpa" {
    type master;
    file "/etc/named/zones/db.192";  # 192.0.0.0/8  subnet
};
```
</div>


**/etc/named/zones/dns.myhome.cf**
```
@       IN      SOA     myhome.cf. admin.dns.myhome.cf. (
```
Put your search domain in here.


```
dns          IN      A       192.168.0.200
*.openshift  IN      A       192.168.0.36
js	         IN        A       192.168.0.4
```
This is the directory of host entries, this can be extended as needed.

<button class="collapsible" id="yaml3">Click here for the complete /etc/named/zones/dns.myhome.cf,</button>
<div class="content" id="yaml3data" markdown="1">
```
@       IN      SOA     myhome.cf. admin.dns.myhome.cf. (
                              3         ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL



; name servers - NS records
    IN      NS      dns

dns          IN      A       192.168.0.200
*.openshift  IN      A       192.168.0.36
js	     IN      A       192.168.0.4
```
</div>


**/etc/named/zones/db.192**
This file contains the diretory for allowing reverse lookups, i.e. looking up a hostname from an IP address.

```
            IN      NS      dns.myhome.cf.
200.0.168	  IN      PTR   dns.myhome.cf.
4.0.168     IN      PTR   js.myhome.cf.
```
This has the same structure as the previous file but it contains PTR instead of A records.


<button class="collapsible" id="yaml3">Click here for the complete /etc/named/zones/db.192,</button>
<div class="content" id="yaml3data" markdown="1">
@       IN      SOA     dns.myhome.cf. admin.dns.myhome.cf. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL



; name servers - NS records
    IN      NS      dns.myhome.cf.
200.0.168	  IN      PTR   dns.myhome.cf.
4.0.168     IN      PTR   js.myhome.cf.
</div>
