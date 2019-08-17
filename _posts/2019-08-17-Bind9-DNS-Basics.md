---
layout: post
date: 2019-08-17 07:00:00
categories: misc
title: "Bind9 DNS Basics"
---

Today I sat down and installed Bind9 to act as a local DNS server. As this took me far to long I have attached a config similar to my home one explaining the changes I made from the default.

<!--more-->


*/etc/named.config*

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
```
</div>
