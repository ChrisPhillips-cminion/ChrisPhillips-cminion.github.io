---
layout: post
date: 2020-3-16 00:01:00
categories: MQ
title: "Enable TLS for ACE HTTPS calls"
author: ["MannieKagan"]
---

When making calls from ACE to https endpoints the trust store must contain the certificate for the target endpoint. In ACE this is done by creating a secret and reference it in the help chart.  This article provides instructions on how to do this.


<!--more-->

1. Log into the ACE Platform

2. Create Server on ace dashboard

3. Add bar containing API REST or SOAP over HTTPS flow (we are concerted here with inbound TLS)

4. Press continue,

5. Click on the Download Configuration Package
This downloads a file config.tar.gz to your browser client machine.

6. Unzip. untar it.
7. Copy generateSecrets.sh -> generateSecret1.sh
8. Edit generateSecret1.sh add line 13 and modify line 146, 147 below
9. Update generateSecret1.sh as in the following examples
```
Add TARGET_SECRET_NAMESPACE=$2
Add -n $TARGET_SECRET_NAMESPACE"
```
10. Edit serverconf.yaml
```yaml
ResourceManagers:
  HTTPSConnector:      
    KeystoreFile: '/home/aceuser/ace-server/keystore.jks'
    KeystorePassword: 'keypass'  
    KeystoreType: 'JKS'           
    TruststoreFile: '/home/aceuser/ace-server/truststore.jks'
    TruststorePassword: 'keypass'
    TruststoreType: 'JKS'           
```

11. Replace zero length files with populated files you generated

12. Copy it to the icp bastion, and run `generateSecrets1.sh`
```
chmod +x generateSecrets1.sh
./generateSecrets1.sh ace-tls-my-secret ace
```
13. Verfy created with:
`oc get secret -n ace | grep tls-my-secret`

14. Check contents of secret with:
`oc get secrets ace-tls-my-secret -n ace -o yaml`

15. Back to ace dashboard step after

16. Press Next
17. Select ‘Toolkit’
18. Next

19. Fill out Helm chart values

## Please note:

Specify name of secret specified in generateSecrets1.sh above

When the server initially starts up it converts the pem and crt in the secret into a JKS keystore with a label or alias corresponding to the name after the dash (‘-‘). Specify the alias here.

Create the server.
After it starts check the logs …….
```
2020-04-29T20:22:50.086Z Integration server not ready yet
An https endpoint was registered on port '7843', path '/salespostingapi/0.1*'.
2020-04-29 20:22:50.199328: The HTTP Listener has started listening on port '7843' for 'https' connections.
2020-04-29 20:22:50.199540: Listening on HTTP URL '/salespostingapi/0.1*'.
Started native listener for HTTPS input node on port 7843 for URL /salespostingapi/0.1*
2020-04-29 20:22:50.199956: Deployed resource 'gen.OrderBotSalesPostingPublic_01' (uuid='gen.OrderBotSalesPostingPublic_01',type='MessageFlow') started successfully.
2020-04-29 20:22:50.200064: About to 'Start' the deployed resource 'OrderBotSalesPostingPublicLib' of type 'StaticLibrary'.
2020-04-29T20:22:55.181Z Integration server not ready yet
2020-04-29T20:23:00.277Z Integration server not ready yet
..2020-04-29 20:23:00.586571: IBM App Connect Enterprise administration security is authentication, authorization file.
2020-04-29 20:23:00.881816: The HTTP Listener has started listening on port '7600' for 'RestAdmin http' connections.

2020-04-29 20:23:00.882746: Integration server has finished initialization.
2020-04-29T20:23:05.377Z Integration server is ready
```

## Troubleshooting:-
1. Log onto the Pod.
`oc exec -ti <podname> -n <namespace>`

### Check the certificate
1. cd /home/aceuser/initial-config
2. ls
3. Verify the converted JKS keystore/truststore
4. cd ~
5. . /opt/ibm/ace-11/server/bin/mqsiprofile
6. cd /home/aceuser/ace-server
7.  keytool -list -storetype JKS -keystore truststore.jks -storepass keypass -v
8. keytool -list -storetype JKS -keystore keystore.jks -storepass keypass -v
9. Validate that the certifiicate is present

### Check the downloaded assets
1. cd /home/aceuser/ace-server
2. ls
`config  keystore.jks  log  overrides  run  server.conf.yaml  ssl  truststore.jks`
3. check the server.conf.yaml override
`cat overrides/server.conf.yaml`

4. See the tls stanza pointing to the keystore/truststore
```yaml
ResourceManagers:
  HTTPSConnector:
    KeystoreFile: /home/aceuser/ace-server/keystore.jks
    KeystorePassword: keypass
    KeystoreType: JKS
    TruststoreFile: /home/aceuser/ace-server/truststore.jks
    TruststorePassword: keypass
    TruststoreType: JKS
RestAdminListener:
  authorizationEnabled: true
  authorizationMode: file
  basicAuth: true
Security:
  Permissions:
    admin: read+:write+:execute+
    audit: read+:write-:execute-
    editor: read+:write+:execute-
    operator: read+:write-:execute+
    viewer: read+:write-:execute-
Statistics:
  Resource:
    reportingOn: true
  Snapshot:
    accountingOrigin: none
    nodeDataLevel: basic
    outputFormat: json
    publicationOn: active
    threadDataLevel: none
UserExits:
  activeUserExitList: ACEOpenTracingUserExit
  userExitPath: /opt/ACEOpenTracing
  ```
