---
layout: post
date: 2020-8-10 00:13:00
categories: APIConnect
title: "Setting the DataPower Password on deployment using ExtraValueFiles"
---

Using K8s Secrets it is possible to set the DataPower so it does not use the default admin/admin password on deployment.  This is true for both v10 and v2018. However it is a little known secret.

<!--more-->

The following is taken from [https://github.com/ibm-apiconnect/charts/blob/develop/stable/dynamic-gateway-service/values.yaml#L61](https://github.com/ibm-apiconnect/charts/blob/develop/stable/dynamic-gateway-service/values.yaml#L61)

```
  # In order to replace the default admin credentials, the new credentials should be configured via Secret and `.Values.datapower.adminUserSecret` must be set to the name of
  # the Secret containing the admin user's credentials
  #
  # The following are properties which can be used to define the admin user's credentials:
  # - `password-hashed`: The hashed value (see Linux `man 3 crypt` for format) of the admin user's password. Required if `password` is not defined.
  # - `password`: The admin user's password. Required if `password-hashed` is not defined; ignored if `password-hashed` is defined.
  # - `salt`: The salt value used when hashing `password` (see `man 3 crypt`). Optional; ignored when `password-hashed` is defined. (Default: 12345678)
  # - `method`: The name of the hashing algorithm used to hash `password`. Valid options: md5, sha256. Optional; ignored when `password-hashed` is defined. (Default: md5)
  #
  # The following examples create Secrets with different values, but result in an admin user with the same credentials (and the same password hash)
  #   kubectl create secret generic admin-credentials --from-literal=password=helloworld --from-literal=salt=12345678 --from-literal=method=md5
  #   kubectl create secret generic admin-credentials --from-literal=password=helloworld
  #   kubectl create secret generic admin-credentials --from-literal=password-hashed='$1$12345678$8.nskQfP4gQ8tk5xw6Wa8/'
  #
  # These two examples also result in Secrets with different values but identical admin credentials
  #   kubectl create secret generic admin-credentials --from-literal=password=hunter2 --from-literal=salt=NaCl --from-literal=method=sha256
  #   kubectl create secret generic admin-credentials --from-literal=password-hashed='$5$NaCl$aOrRVimQNvZ2ZLjnAyMvT3WgaUEXoWgwkgyBrhwIg04'
  #
  # Notice that, when setting `password-hashed`, the value must be surrounded by single-quotes
  #
  # In all of the examples above, `.Values.datapower.adminUserSecret` should be set to 'admin-credentials' for the admin user to be configured.
  adminUserSecret:
```

1. Create the secret as described above
2. Create or extend a file called `dp-extravaluesfile.yaml` in the `APICUP` project directory
3. Add the following lines into the file
```
datapower:
  adminUserSecret <name of secret>
```

4. To add the extra values file to the `APICUP` config tun the following Command
`apicup subsys set <gwy> extra-values-file <path to dp-extravaluesfile.yaml>`


5. Run this command to install the helm chart `apicup subsys install <gwy>`
