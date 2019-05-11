---
layout: post
date: 2018-02-26  00:00:00
categories: APIConnect
title: 'Guest Post: APIC Gateway delayed analytics data \[Craig S\]'
---

Guest Post: APIC Gateway delayed analytics data \[Craig S\] 
===========================================================

 
So this post is stolen with permission from Craig Simmons IBM
(https://www.linkedin.com/in/craig-simmons-1b67436b/)


 
 
 

------------------------------------------------------------------------


 
 
### Guest Post: APIC Gateway delayed analytics data \[Craig S\] 

So this post is stolen with permission from Craig Simmons IBM
(<https://www.linkedin.com/in/craig-simmons-1b67436b/>)

So we have several DR's amongst us (DR = Dashboard Refresher). These
good folk are refreshing their charts every 30 seconds or thereabouts.
As a result it's come to their attention yesterday morning that for
several hours no data was being delivered to their dashboards. Though
initially they thought this data was appearing later it appears the data
was lost. So we need to troubleshoot what's going on, particularly as
the same thing happened the following day during a similar window, but
with differing start and end times.

So a PMR was raised (02305,001,866) and the logs sent for analysis. In
the meantime (thanks to Chris Phillips) I invoked a rest call against
the catalog. This call pulls back 'recent' data from the Kibana database
in the APIC Management cluster. I'm guessing it returns x number of
recent rows. It doesn't for obvious reasons, attempt to boil the ocean
and return everything.

The call takes on the following syntax: -

``` 
https://<APIMF5>/v1/orgs//environments//events
```

where

\<APIMF5\> is the loadbalancer in front of the APIC Management cluster.
Of you're not using n LB, go straight to the management host

 = the organisation short name

 = the catalog name (environments are APIC 'old speak' for
catalogs

A quick way to obtain these ID's to flesh out your call is to: -

Log in to the APIM Manager, select your organization top right, hit the
'menu' item top left, Dashboard, and click on the 'paperclip' icon
underneath the appropriate catalog. This returns the catalog identifier,
something like: -

``` 
apic config:set catalog=apic-catalog://apic-mgt.service.group/orgs/jobloggscompany-prd/catalogs/prod1
```

So the rest string derived from this info would be: -

``` 
https://<APIMF5>/v1/orgs/jobloggscompany-prd/environments/prod1/events
```

You'll then be asked for credentials. After this, your data is returned
as a JSON object. It will look something like this (some data obfuscated
for obvious reasons): -

``` 
/consent-preferences”,”spaceId”:””,”spaceName”:””,”timeToServeRequest”:26,”bytesSent”:2,”requestProtocol”:”https”,”requestMethod”:”GET”,”uriPath”:”/
<SNIP>
```

So what does this tell us?

1\. The database is up

2\. Non corrupted and readable data is being returned

3\. A recent timestamp of data written to the database (14:42 in this
case)

So we can compare this with the dashboards. Do they reflect the same
date/time? Do they reflect a similar amount of total calls (in this case
1660929)

If that's NOT the case, we have some form of problem at the dashboards.
i.e. they are not reflecting the content of the database. If the two
concur, it's a case of troubleshooting why the data is not being pushed
from the Gateway in a timely fashion....

Update 21/02/18

I witnessed a 'live' failure via the rest call above. The dashboard
showed a similar response. So we can determine that the problem lay
somewhere between the gateway and the management cluster, it is NOT a
case of the dashboards not reflecting the database content.

The details were: -

``` 
1552:53.588 — last analytics data received
```

``` 
1643 data received timestamped 15:52:55.186
```

``` 
1646 data received timestamped 15:52:55.875
```

``` 
1649 data received timestamped 15:52:56.746
```

``` 
1659 — data now arriving ‘real time’ but ‘hole’ since last transmission at 1552:56.746
```

So now we have a failure window we can obtain the APIC and DataPower
logs

So APIC first. We are going to look at the following file: -

``` 
/var/log/apim_rproxy_access.log
```

Update 22/02/18

Received PMR response as follows: -

``` 
NODE03 logstash is in an error state showing the below error since 2018–02–14 15:28:05: 
```

``` 
2018–02–21 09:27:03 +0000: Read error: #<IOError: No space left on device>
/opt/logstash/vendor/jruby/lib/ruby/shared/tmpdir.rb:144:in `create’
org/jruby/ext/tempfile/Tempfile.java:96:in `initialize19'
org/jruby/RubyIO.java:871:in `new’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/client.rb:140:in `setup_body’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/client.rb:178:in `try_to_finish’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/client.rb:101:in `reset’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/server.rb:414:in `process_client’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/server.rb:400:in `process_client’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/server.rb:270:in `run’
org/jruby/RubyProc.java:281:in `call’
/opt/logstash/vendor/bundle/jruby/1.9/gems/puma-2.16.0-java/lib/puma/thread_pool.rb:106:in `spawn_thread’
```

``` 
In order to address the above, a reboot of the nodes is required as soon as possible. Please reboot one node at a time and wait for that node to fully reboot and is fully back up before working on the others. As NODE01 is your Primary node for Informix cluster I would advise to reboot it last — you may consider to elect another node to be Primary during the reboot of NODE01 to minimize the failover time for another node to become Primary.
```

``` 
As logstash is one of the processes responsible for receiving analytic data from the DataPower Gateway the above issue explains your gap in receiving data and not being able to visualize those.
```

``` 
This problem is a likely known issue tracked by APAR LI79840, which is fixed in v5.0.8.2. The workaround recommended, until you are ready to upgrade, is the reboot your Management Nodes every 60 days so that you will trigger a clean up of the space under the temporary directory.
```

``` 
If you upload the last management server logs (likely named NODE02) I can check its state as well, although a reboot of that one as well is probably the best course of action.
```

``` 
Please let me know if you have additional questions about this case.
```

A question I had was in relation to which log file the above info was
gleaned from; the answer being: -

``` 
/var/log/logstash.log
```

So case closed. No requirement to analyse the DataPower logs, which we'd
already looked through, and we believe DataPower is very much 'push and
forget' in terms of analytics delivery, and likewise, no detailed
analysis of the apim\_rproxy\_access.log in the same directory as the
logstash.log file. however, its worth noting that when we did look
through it, we noticed '404' errors around the dates/times of the
outages





By [Chris Phillips](https://medium.com/@cminion) on
[February 26, 2018](https://medium.com/p/47171f13b91f).

[Canonical
link](https://medium.com/@cminion/guest-post-apic-gateway-delayed-analytics-data-craig-s-47171f13b91f)

Exported from [Medium](https://medium.com) on April 6, 2019.
