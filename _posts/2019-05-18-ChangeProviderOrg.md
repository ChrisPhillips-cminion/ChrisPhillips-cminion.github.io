---
layout: post
date: 2019-05-18  20:57:00
categories: APIConnect
title: 'Changing Provider Organisation Owner in APIConnect 2018 [Guest Post by Nick Cawood]'
---
*This is a guest post by Nick Cawood*


In API Connect 2018.4.1.X the Management UIs do not support changing the owner of a Provider Organisation. Therefore to change the ownership the APIC Toolkit should used, and specifically the orgs transfer owner commands.

To change the owner of a Provider Organisation firstly the new owner needs to be a member of the Provider Organisation. The APIC Toolkit is then used by logging into the Management Server, getting the new owner’s “associate” detail, then transferring the ownership and finally logging out of the Management Server.


Firstly login

`$ ./apic login --server platform.AAA.BB.CC.DD.nip.io --username EXISTING_OWNER --password PASSWORD --realm provider/default-idp-2`

Logged into platform.AAA.BB.CC.DD.nip.io successfully

```
$ ./apic associates:list -s platform.AAA.BB.CC.DD.nip.io --scope org -o <ProviderOrganisationName>

NewUser   https://platform.AAA.BB.CC.DD.nip.io/api/orgs/0be9e33f-ca5f-4b66-931f-ebadc7f55bd8/associates/5df801b9-836c-4a94-a451-b8cd364d9736   
OriginalUser   https://platform.AAA.BB.CC.DD.nip.io/api/orgs/0be9e33f-ca5f-4b66-931f-ebadc7f55bd8/associates/a40df1ef-dc42-4457-a7d9-a2fe9a76ce98
```

Add new user to a file, `example.yaml`:
```
new_owner_associate_url:  https://platform.AAA.BB.CC.DD.nip.io/api/orgs/0be9e33f-ca5f-4b66-931f-ebadc7f55bd8/associates/5df801b9-836c-4a94-a451-b8cd364d9736
```

Run the commands

```
$ ./apic orgs:transfer-owner -s platform.AAA.BB.CC.DD.nip.io <ProviderOrganisationName> exam-ple.yaml

<ProviderOrganisationName>    [staplatform.AAA.BB.CC.DD.nip.iote: enabled]   https://platform.AAA.BB.CC.DD.nip.io/api/orgs/0be9e33f-ca5f-4b66-931f-ebadc7f55bd8
```


### Knowledge Center Links
https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.toolkit.doc/rapic_cli_login.html

https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.cliref.doc/apic_login.html

https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.cliref.doc/apic_associates_list.html

https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.toolkit.doc/rapim_cli_mgmt-commands.html

https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.cliref.doc/apic_orgs_transfer-owner.html

https://www.ibm.com/support/knowledgecenter/SSMNED_2018/com.ibm.apic.cliref.doc/apic_logout.html
