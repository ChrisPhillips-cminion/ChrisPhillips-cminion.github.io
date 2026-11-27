---
layout: post
date: 2026-11-27 09:00:00
categories: APIConnect
title: "`apic draft-apis:create` Fails on Re-Run: Name+Version Uniqueness from Drafts to Catalogs"
author: ["ChrisPhillips", "IBMBob"]
description: "In API Connect, name+version is the identity of an API or a product — in the provider org for drafts, and in each catalog and space for published resources. `apic draft-apis:create` enforces it and fails on re-run, and the reference page documents neither the rule, the conflict workflow, nor the fact that the command family is deprecated."
tags: [APIConnect, CLI, apic, DraftAPIs, Products, Automation, Documentation]
draft: true
---

I have been driving this toolkit for the better part of a decade, and it took re-running a create step against an environment that was not clean to remind me that `apic draft-apis:create` is not idempotent — and that the rule behind that failure is not a draft quirk. It is the identity model for every API and product in the system.

<!--more-->

## What happened

A script did exactly what the `apic draft-apis:create` reference page says: create a draft API in a provider org from a definition file. An earlier run had left a draft behind in the org. The next run failed against that leftover:

```bash
apic draft-apis:create --org "acme-provider-org" \
  --server "https://api.mgmt.example.com" \
  "orders-api.yaml"
```

```
WARNING: The command draft-apis is deprecated and will be removed in future release.
Error: The Draft API cannot be created with name 'orders-api' and version '1.0.0'. Another resource of type draft_api (id: 985e2fb2-1e20-4a90-8f91-cf3e533eafed) already exists with the same name and version.
```

The script had checked that the org existed before running the step. Nothing checked for the draft, because nothing in the documentation suggested it needed to. The create step had passed the first time and failed every time after.

## The rule — and it is not about drafts

Draft APIs are identified by name + version within the provider org. The name and version come from the API definition — for an OpenAPI document, `info.title` and `info.version`.

- Same name, different version: two drafts, both valid, side by side.
- Same name, same version: one draft. The second `create` is a conflict.

`orders-api:1.0.0` and `orders-api:2.0.0` coexist happily. A second `orders-api:1.0.0` does not.

That is not a quirk of the draft workspace. Name + version is the identity of an API everywhere it exists, and of a product too — in the provider org, and again in every catalog and space it is published to. Once you know that, the behaviour on the published side stops being surprising and starts being predictable.

## Draft products follow the same rule

Products are identified by name + version within the provider org as well. `apic draft-products:create` enforces the same uniqueness and fails the same way when the name+version is already taken. Everything in the conflict-resolution section below applies to products exactly as it does to APIs, with `draft-products` in place of `draft-apis`.

## Published products

Publishing moves the rule, it does not drop it. Within a catalog — or a space, if you publish into one — a product is unique by name + version.

What changes on the published side is what a collision means. Publishing a product whose name+version is already in the catalog does not fail the way `draft-apis:create` does: it replaces the existing product in place. The replacement is guarded by plan compatibility — every plan in the existing product that carries active subscriptions must still exist in the new definition, or the publish is refused. That guard is the point. A replace is not allowed to quietly strand consumers.

Publish a different version — `orders-product:2.0.0` against an existing `orders-product:1.0.0` — and the two sit side by side as separate products. Moving subscriptions from the old version to the new one is a separate, deliberate step; it does not happen just because you published.

## Published APIs

APIs in a catalog are unique by name + version too, and this is where the rule reaches people who have never opened the draft workspace. When you replace a product, an API with the same name+version is updated in place — the consumers of that product see the new definition without doing anything.

The sharper edge is a second product. If you publish a product containing an API whose name+version is already in the catalog inside a different product, the catalog does not gain a second copy: the new product consumes the existing API. One API, two products referencing it. That is documented behaviour, not an accident, and it has consequences:

- Publishing product B changes the API that product A's consumers are calling, if B ships the newer definition.
- Deleting product A does not remove the API, because B still references it.

If you wanted two independent APIs, you need two name+versions. If you wanted one API shared across products, this is the mechanism — but you should know you are using it.

## Why it matters

A create step that passes once and fails on re-run is not a procedure. Scripts get re-run against environments that are not clean — that is their entire purpose — and anything automated around the toolkit hits the same wall in CI. A reference page for a create command that stops before "when the resource already exists" produces scripts that pass exactly once. And the reference pages are no better on the published side: the uniqueness rule, the replace-on-conflict behaviour, plan compatibility, and API consumption are all stated nowhere a person writing a script would think to look.

## Resolving the conflict

Three options, depending on what the existing draft is. The same three, with `draft-products` commands, resolve a product conflict.

### The draft is stale — delete and re-create

```bash
# see what is already there
apic draft-apis:list --org acme-provider-org

# remove the conflicting draft
apic draft-apis:delete --org acme-provider-org orders-api:1.0.0

# the original create now succeeds
apic draft-apis:create --org acme-provider-org orders-api.yaml
```

Check whether a draft product references the API before deleting it.

### The draft is the one you are iterating on — update it

```bash
apic draft-apis:update --org acme-provider-org orders-api.yaml
```

`update` replaces the definition of the existing draft. Same name, same version, no conflict, no delete.

### You genuinely want a new version

Bump `info.version` in the definition and create. Both versions sit side by side as drafts. That is what the version is for.

## The deprecation nobody mentions either

Read the error output again. The first line is not the conflict — it is the CLI warning that the entire `draft-apis` command family is deprecated and will be removed in a future release. The reference pages do not mention that either, and the same warning prints on the `draft-products` family. So the documented procedure for creating draft APIs is a procedure for a command the toolkit itself says is going away, and the docs say nothing about either half of that sentence.

## Limitations and Notes

- Behaviour verified on the 12.0.x CD toolkit; the reference pages checked were from the 12.1.x CD documentation set.
- `draft-apis:create` has no overwrite flag. Delete, update, or change the version — there is no fourth way.
- The catalog-side behaviour — replace on same name+version, the plan compatibility guard, API consumption — is the documented model for v10 and later. Verify the details against your own fix pack before scripting around them.

I will find out what else I have failed to write down the next time a script collides with its own leftovers.
