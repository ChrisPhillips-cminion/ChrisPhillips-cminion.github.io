---
layout: post
date: 2026-11-28 18:00:00
categories: APIConnect
title: "apic CLI: fixing commands that fail with 'unknown command'"
author: ["ChrisPhillips", "IBMBob"]
description: "You copy an apic command from the documentation or an old runbook and the toolkit rejects it. The install is fine — the name is wrong. 22 command names that don't match the toolkit binary, the commands that work instead, and three patterns to fix any name not on the list."
tags: [APIConnect, CLI, apic, Troubleshooting]
draft: true
image: /images/apic-unknown-command.png
---

You copy an `apic` command out of the documentation or an old script, and the toolkit rejects it. The install is fine — the name is wrong. Here is the map of command names that don't match the toolkit, and what to run instead.

<!--more-->

## The error looks like this

```
Error: unknown command "analytics" …
Did you mean this?
        analytics-services, analytics-services:clear, …
```

The `Did you mean this?` list usually contains the fix. When it doesn't, check the table below — it comes from checking every command name the documentation lists against the toolkit binary (build `1c4941eb…`, 969 commands across the seven modes): 22 documented names do not match.

## Command names that don't match

| Name that fails | Command that works | Where the name comes from |
|---|---|---|
| `apic analytics` | `apic analytics-services …` | CLI reference §21 |
| `apic analytics:create` | no equivalent | CLI reference §22 |
| `apic lb4` | no equivalent | CLI reference §277 |
| `apic monitor` | no equivalent | CLI reference §311 |
| `apic export`, `apic import` | `apic projects:export`, `apic projects:import` | API Studio §6.4.21.1 |
| `apic content:list-type` | `apic content:list-types` | devportal §10.3.2 |
| `apic maintenance:rebuild_node_access` | `apic maintenance:rebuild-node-access` | devportal §10.3.2 |
| `apic maintenance:search_api_index_rebuild` | `apic maintenance:search-api-index-rebuild` | devportal §10.3.2 |
| `apic maintenance:search_api_index_status` | `apic maintenance:search-api-index-status` | devportal §10.3.2 |
| `apic apps:publish` | no `apps:publish` — see `apps --help` | toolkit §7.4.3.1 |
| `apic integrations:clear-all` | `apic integrations:clear`, `apic integrations:list-all` | toolkit §7.4.3.4 |
| `apic catalog:create`, `apic catalog:get` | `apic catalogs:create`, `apic catalogs:get` | toolkit §7.4.3.5 |
| `apic catalogs:set` | `apic catalogs:update` | toolkit §7.4.3.5 |
| `apic tasks:clear`, `tasks:create`, `tasks:delete` | only `tasks:get/list/update` exist | toolkit §7.4.3.5 |
| `apic user-registry-settings:delete` | only `get/update` exist | toolkit §7.4.3.5 |
| `apic draft-products:publish-all` | `apic draft-products:publish` | toolkit §7.4.3.5 |
| `apic drafts:validate` | `apic draft-apis:validate` | toolkit §7.4.3.6, §7.13.10 |
| `apic publish` | `apic products:publish`, `apic projects:publish` | toolkit §7.4.3.7, §7.4.3.9, §7.13.4 |

## Three patterns to try first

If your failing command is not in the table, try these in order — they catch most mismatches:

1. **Pluralise the object.** `catalog:create` → `catalogs:create`.
2. **Swap underscores for hyphens.** `search_api_index_rebuild` → `search-api-index-rebuild`.
3. **Check the real object name.** `apic export` is not a thing; the project commands are `projects:export` and `projects:import`.

## Two that catch people out

**`apic drafts:validate`.** There is no `drafts` object — the command is `apic draft-ais:validate`:

```bash
apic drafts:validate     # no
apic draft-apis:validate  # yes
```

And note the CLI now flags the whole `draft-apis` family as deprecated, warning it will be removed in a future release — I wrote up the draft API create/delete workflow around that warning [here]({% link _posts/2026-11-27-apic-draft-api-name-version-conflict.md %}).

**Plain `apic publish`.** There is no plain publish. To publish a product, use `apic products:publish`; to publish a project, `apic projects:publish` — with `--stage` if you only want to stage it into a catalog.

## If you build scripts from the documentation

Any automation assembled from documented command lists inherits these names — and the failure mode is unhelpful, because an unknown command looks like a broken toolkit install rather than a bad name. If you generate scripts or runbooks from the docs, validate the command names against the binary's own help output first; it is the authoritative list of what exists.

## Summary

22 command names in the documentation do not match the toolkit binary: four reference pages for commands with no equivalent, singular/plural drift, underscore/hyphen drift, and a plain `apic publish` that never existed. When a command fails, read the `Did you mean this?` suggestion first, then apply the three patterns — pluralise, hyphenate, check the object name.

## Limitations and Notes

- Verified against toolkit build `1c4941eb…` (built 2026-11-04), the 12.0.x CD binary, against the 12.1.x documentation set. Command names can change between releases.
- Command names only — flags and arguments are a separate matter and fail differently.
- The reverse also exists: the toolkit implements commands the documentation doesn't list. A topic for another post.
