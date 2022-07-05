---
layout: post
categories: APIConnect
date: 2022-07-05 00:14:00
author: ["kaizhang"]
title: API Connect v5 to v10 Incremental Migration
draft: true
---

The initial migration from v5 to v10 might take time from days to weeks, or even longer. During the period, the v5 instance might have evolved. Hence, customers often require to bring the changes to the migrated v10 instances. Here we discuss a few scenarios and approaches to handle them accordingly.
<!--more-->

## Customer Scenarios and Approaches:
There are 3 types of delta that could happen in v5 during in the window between subsequent migrations -
* `new` artifacts, like new APIs / products / apps / subscriptions, etc.
* `modified` artifacts
* `deleted` artifacts

| Migration Approaches | Types of delta supported (v5 impacts) | v10 impacts |
| ------ | ------ | ------ |
| Approach 1: `Freeze v5 instances`| Freeze / no changes allowed in v5 | Allow changes (`new, modified, deleted`) in v10 |
| Approach 2: `Incremental migration`| Allow adding `new` artifacts in v5 | Allow changes (`new, modified, deleted`) in v10 |
| Approach 3: `Wipe out and Remigrate`| Allow `new, modified, deleted` in v5 | All changes (`new, modified, deleted`) in v10 will be lost. |
| Approach 4: `Delta Migration`| Allow `new, modified, deleted` in v5 | Changes to `modified & deleted` v5 artifacts will be overwritten. All other changes will be kept. |

### Approach 1: Freeze v5 instances

Summary:

- This is the simplest approach.
- Freezes v5 instances during migration period.
- And cut over to migrated v10 instances when they are ready to take over.

Applicable Scenarios:

- the migration period is relative short.
- v5 instances do not change often, like a production env.

Implementation Details:

- Just switch developers and consumers to v10 at the cutover.

### Approach 2: Incremental migration

Summary:

- Partially freeze v5 instances during migration period. Allow only additions of new artifacts in v5.
- Do one or more incremental migrations using AMU before the cutover to v10

Applicable Scenarios:

- Production envs can often freeze new developments. But cannot afford to freeze onboarding new users.
- This approach can leverage AMU to incrementally migrate new consumer orgs, applications, subscriptions added to v5 during migration window.

Implementation Details:

- allow v5 instances to continue to add new artifacts, onboard new consumers before the cutover to v10
- At the cutover, take another dbextract from v5
- Apply the same AMU unpack, mappings / modifications on the new dbextract
- Make necessary additional changes on the new artifacts if needed
- Run another AMU push to the same v10 instance.

### Approach 3: Wipe out and Remigrate Again

Summary:

- No freeze on v5. Allow it evolves independently.
- Wipe out v10 instance or affected provider orgs. Redo the migration.

Applicable Scenarios:

- cannot freeze v5. During the migration window, artifacts can be changed, added and removed, like a dev envs often cannot be frozen for an extended period.
- There are NO significant changes in the v10 instance after initial migrations.

Implementation Details:

- allow v5 instances to continue to evolves independently before the cutover to v10
- At the cutover, take another dbextract from v5
- Apply the same AMU unpack, mappings / modifications on the new dbextract
- Make necessary additional changes on any artifacts if needed
- Delete and recreate the providers orgs in the v10 instance that are impacted (assuming no cmc changes).
- Run an AMU push to the v10 instance.


### Approach 4: Delta Migration

Summary:

- No freeze on v5. Allow it evolves independently.
- Run a delta migration to sync up the changed, newly added, removed artifacts to v10

Applicable Scenarios:

- cannot freeze v5. During the migration window, artifacts can be changed, added and removed.
- There are significant changes in the v10 instance after initial migrations. Hence v10 provider orgs cannot be wiped out.

Implementation Details:

- allow v5 instances to continue to evolves independently before the cutover to v10
- At the cutover, take another dbextract from v5
- Apply the same AMU unpack, mappings / modifications on the new dbextract
- Do a dry-run with Run delta-migration tool to list and examine the delta of artifacts
- Make necessary additional changes on changed or new artifacts if needed
- Push / sync up the delta to the v10 instance by running the delta-migration tool.

Refer to the [delta-migration tool doc](README.md) for details on how to use it.
