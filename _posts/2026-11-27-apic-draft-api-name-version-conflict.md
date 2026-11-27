---
layout: post
date: 2026-11-27 09:00:00
categories: APIConnect
title: "GAP-020: `apic draft-apis:create` and the name+version rule the reference page doesn't mention"
author: ["ChrisPhillips", "IBMBob"]
description: "Draft APIs in API Connect are unique by name+version per provider org. `apic draft-apis:create` enforces it and fails on re-run — and the reference page documents neither that, the conflict workflow, nor the fact that the command family is deprecated. I hit it in my own runbook."
tags: [APIConnect, CLI, apic, DraftAPIs, Automation, Documentation]
image: /images/gap020-draft-api-conflict.png
---

I have been driving this toolkit for the better part of a decade, and it took re-running my own runbook on a Tuesday morning to remind me that `apic draft-apis:create` is not idempotent — and that I had never written that down either.

<!--more-->

## What happened

I run my runbooks against a live environment on chrisai2 to check they still work. The runbook `src-157-create-a-draft-api` was written from the `apic draft-apis:create` reference page in the SSMNED 12.1.x CD documentation set, and it does exactly what that page says. An earlier run had left a draft API behind in the org. On 26 November the runbook failed against that leftover:

```bash
apic draft-apis:create --org "molor3-provider-org" \
  --server "https://api.mgmt.example.com" \
  "certify-work/cert-draft-api-file-draft-api-file.yaml"
```

```
WARNING: The command draft-apis is deprecated and will be removed in future release.
Error: The Draft API cannot be created with name 'cert-draft-api' and version '1.0.0'. Another resource of type draft_api (id: 985e2fb2-1e20-4a90-8f91-cf3e533eafed) already exists with the same name and version.
```

The runbook had probed the org before running the step — it existed. Nothing probed for the draft, because nothing in the documentation suggested it needed to. The failure was filed as GAP-020, classified as missing cleanup.

## The rule

Draft APIs are identified by name + version within the provider org. The name and version come from the API definition — for an OpenAPI document, `info.title` and `info.version`.

- Same name, different version: two drafts, both valid, side by side.
- Same name, same version: one draft. The second `create` is a conflict.

`cert-draft-api:1.0.0` and `cert-draft-api:2.0.0` coexist happily. A second `cert-draft-api:1.0.0` does not.

The reference page for `draft-apis:create` gives the usage line, the flag list, and a list of fields that are allowed but ignored. It does not mention the uniqueness rule, a pre-check for an existing draft, cleanup after the step, or the error you get when you trip over one. The runbook I wrote from it inherited every one of those omissions.

## Why it matters

A create step that passes once and fails on re-run is not a procedure. Runbooks get re-run against environments that are not clean — that is their entire purpose — and anything scripted around the toolkit hits the same wall in CI. A reference page for a create command that stops before "when the resource already exists" produces scripts that pass exactly once.

## Resolving the conflict

Three options, depending on what the existing draft is.

### The draft is stale — delete and re-create

```bash
# see what is already there
apic draft-apis:list --org molor3-provider-org

# remove the conflicting draft
apic draft-apis:delete --org molor3-provider-org cert-draft-api:1.0.0

# the original create now succeeds
apic draft-apis:create --org molor3-provider-org \
  certify-work/cert-draft-api-file-draft-api-file.yaml
```

Check whether a draft product references the API before deleting it.

### The draft is the one you are iterating on — update it

```bash
apic draft-apis:update --org molor3-provider-org \
  certify-work/cert-draft-api-file-draft-api-file.yaml
```

`update` replaces the definition of the existing draft. Same name, same version, no conflict, no delete.

### You genuinely want a new version

Bump `info.version` in the definition and create. Both versions sit side by side as drafts. That is what the version is for.

## The deprecation nobody mentions either

Read the error output again. The first line is not the conflict — it is the CLI warning that the entire `draft-apis` command family is deprecated and will be removed in a future release. The reference pages do not mention that either, and the same warning prints on the `draft-products` family. So the documented procedure for creating draft APIs is a procedure for a command the toolkit itself says is going away, and the docs say nothing about either half of that sentence.

## What changed

GAP-020 is filed against the source page so the defect is tracked upstream of me. The runbook case now carries the conflict handling with the create step: list for an existing draft, delete or update according to what it is, then create. The second run of the case passes, which is the standard a runbook has to meet.

## Limitations and Notes

- Behaviour verified on the 12.0.x CD toolkit, against the SSMNED 12.1.x documentation set the runbooks were written from.
- `draft-apis:create` has no overwrite flag. Delete, update, or change the version — there is no fourth way.
- The same name+version uniqueness applies to draft products. `draft-products:create` has the same blind spot in the docs, and the same deprecation warning.

I will find out what else I have failed to document the next time a runbook collides with its own leftovers.
