---
layout: post
date: 2019-07-28 12:00:00
categories: Kubernetes
title: "OpenShift Error - no attribute oo_first_master"

---
<!--more-->

When running the ansible playbooks I got the following error message.

```
fatal: [hostname]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'dict object' has no attribute 'oo_first_master'\n\nThe error appears to be in './openshift-ansible/playbooks/init/version.yml': line 20, column 5, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n  tasks:\n  - set_fact:\n    ^ here\n"}
```

This was caused by having broken my inventory file. I had done a string replace to change master to the hostname of my master. This meant I accidentally had modified the section heading for `[master]` if you are seeing this error check your inventory file has the correct headings.
