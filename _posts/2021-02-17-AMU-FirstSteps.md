---
layout: post
categories: APIConnect
date: 2021-02-17 00:14:00
title: v5->v10 Assessing the impact of a migration
---

Migrating from API Connect v10 from v5 is a common practice right now. Customers are always asking how they can evaluate if any customer work is required to move to either v5c or the native gateway.

<!--more-->

Once you have entitlement for API Connect v10 you can download the AMU tool from PPA or fix central.

This tool has a number of functions.
1. Extract a v5 export and convert the content to v5c. (APIs, Applications, Consumer Orgs, everything really)
2. Take v5c APIs and convert for the new API Gateway
3. Loads the converted data from step 1 and/or step 2 into an a target APIConect v10 system.


1 and 2 can be used to evaluate if any work needs to be done to the APIs prior to having an API Connect v10 running.

To do this you must have API Connect v5 on the latest firmware.

1. Log into the v5 CLI and run `dbExtract` to export the data in an unencrypted form for the AMU to use.
2. Copy dbExtract.tar.gz to the same system AMU is installed on
3. Run the amu `archive:unpack` function to extract and complete the v5c conversion. This may take several hours depending on the size of the v5 estate.
4. Evaluate any errors that this throws. These errors will show any additional work that should be completed in v5 and a new dbExtract taken.
5. Run the amu `archive:port-to-apigw` against the export data.
6. Evaluate any errors that this throws.

In order to fix all errors from `archive:unpack` steps 1-3 may need to be run after each set of changes to v5. However in the majority of use cases no errors are seen here.

The errors from `archive:port-to-apigw` are usually fixable on the file system by modifying the convert APIs.


To see the full whitepaper on AMU Migration please take a look at this whitepaper [https://community.ibm.com/community/user/middleware/viewdocument/api-connect-migration-utility-amu](https://community.ibm.com/community/user/middleware/viewdocument/api-connect-migration-utility-amu)
