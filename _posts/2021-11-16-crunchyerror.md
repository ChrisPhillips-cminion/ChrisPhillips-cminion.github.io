---
layout: post
date: 2021-11-23 00:13:00
categories: APIConnect
title: "Back up failing with exit code 50"

---

When configuring the backup facility of APIC 10.0.1.4 I ran into this error message

```
time="2021-11-23T11:46:06Z" level=info msg="crunchy-pgbackrest starts"
time="2021-11-23T11:46:06Z" level=info msg="debug flag set to false"
time="2021-11-23T11:46:06Z" level=info msg="backrest backup command requested"
time="2021-11-23T11:46:06Z" level=info msg="command to execute is [pgbackrest backup --stanza=db --type=full --repo1-retention-full=1 --repo1-retention-archive=1 --db-host=172.30.222.142 --db-path=/pgdata/management-sjc-postgres]"
time="2021-11-23T11:46:08Z" level=info msg="output=[]"
time="2021-11-23T11:46:08Z" level=info msg="stderr=[ERROR: [050]: unable to acquire lock on file '/tmp/pgbackrest/db-backup.lock': Resource temporarily unavailable\n       HINT: is another pgBackRest process running?\n]"
time="2021-11-23T11:46:08Z" level=fatal msg="command terminated with exit code 50"
```

Validate the credentials you have stored in the mgmt backup secret are correct.
