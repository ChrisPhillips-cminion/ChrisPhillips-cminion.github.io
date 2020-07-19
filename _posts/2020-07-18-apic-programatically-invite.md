---
layout: post
date: 2020-7-18 00:13:00
categories: APIConnect
title: "APIConnect v10 - Programmatically inviting a new user to a consumer org. "
---

I have recently been asked by two customers how they can bulk register a number of user. There are two ways of doing this. Either by sending out an invitations or by creating the user accounts. Though both of these are listed below I recommend that only member invitations are used as it means that passwords are not exposed.

<!--more-->

## Shell script to create  a member invitiation.

When a member invitation is created it invites the a user to join an existing organization. In this sample below it is used to invite a user to a consumer org.


```
#The following paramters need to be set for the user you are creating, this exmaple assumes you are loading them into the local user registry
email=user@cminion.cf

#These paremeters are global for accessing the provider org selecting which consumer org ot add the user to.
consumer_org=fred

porg_username=chrisp
porg_password=chrisp
porg_realm=provider/default-idp-2
catalog=sandbox
org=dev
server=https://manager.v10-k8s2-0002.eu-gb.containers.appdomain.cloud
apic_cli=/usr/local/bin/apic-slim

$apic_cli login -s $server -u $porg_username -p $porg_password --realm $porg_realm

memberin=$(cat <<EOF )
{
    "type": "member_invitation",
    "api_version": "2.0.0",
    "title": "$email",
    "scope": "consumer_org",
    "email": "$email",
    "org_type": "consumer_org",
    "consumer_org_url": "$server/api/consumer-orgs/$org/$catalog/$consumer_org"
}
EOF

echo $memberin | jsonlint-php
echo $memberin > memberin.json

$apic_cli member-invitations:create  -o $org -s $server --scope consumer-org -c $catalog --consumer-org $consumer_org memberin.json
```


In order to use this to bulk load users a simple the above code can be looped over a list of email addresses.


## Shell Script to add a new user to a consumer org
If you are unable to add via an invitation the following code will create a new user and add them to an existing consumer org.

```bash

# The following paramters need to be set for the user you are creating, this example assumes you are loading them into the local user registry
username=$(date +%s)
pass=password123
email=$username@bob.com
fname=fname
lname=lname


#These paremeters are global for accessing the provider org selecting which consumer org ot add the user to.
porg_username=chrisp
porg_password=chrisp
porg_realm=provider/default-idp-2
consumer_org=fred
catalog=sandbox
org=dev
server=https://manager.v10-k8s2-0002.eu-gb.containers.appdomain.cloud


apic-slim login -s $server -u $porg_username -p $porg_password --realm $porg_realm

user=$(cat <<EOF )
{  "type": "user",
  "api_version": "2.0.0",
  "name": "$username",
  "title": "$username",
  "username": "$username",
  "identity_provider": "$catalog-idp",
  "email": "$email",
  "first_name": "$fname",
  "last_name": "$lname",
  "password" : "$pass"}
EOF


echo $user | jsonlint-php
echo $user > usertemp.json

apic-slim users:create  -o $org -s $server --user-registry $catalog-catalog usertemp.json

member=$(cat <<EOF )
{ "type": "member",
"api_version": "2.0.0",
"id": "7a5f6ba0-3908-4ef3-8268-026af6c25b2e",
"name": "$username",
"title": "$username",
"scope": "consumer_org",
"user": {
  "url":"$server/api/user-registries/$org/sandbox-catalog/users/$username"
}}
EOF

echo $member | jsonlint-php
echo $member > member.json

apic-slim  members:create  -s $server  --catalog $catalog --org $org --consumer-org  $consumer_org --scope consumer-org member.json
```
