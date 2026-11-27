---
layout: post
date: 2026-11-28 15:00:00
categories: APIConnect
title: "Restoring an archived governance ruleset in API Connect"
author: ["ChrisPhillips", "IBMBob"]
description: "How to manage the governance ruleset lifecycle in the API Connect Cloud Manager: why published rulesets are immutable, why archived rulesets vanish from the table, and how to restore one."
tags: [APIConnect, Governance, CloudManager, APIGovernance]
draft: true
image: /images/ruleset-lifecycle-restore.png
---

A governance ruleset that disappears from the Cloud Manager is almost always archived, not deleted. Archived rulesets are hidden from the table by default, and the filter that controls that is easy to miss.

This article covers the ruleset lifecycle, how to make archived rulesets visible, and how to restore one.

<!--more-->

## The governance ruleset lifecycle

Custom governance rulesets move through three states: **Draft → Published → Archived**.

The state you cannot leave is Published — in the sense that you cannot change it in place. Once a ruleset is published it is immutable, and any other change means creating a new version with the **Save as new ruleset** option. That strictness is deliberate: scans are run against a specific version of a ruleset, and keeping published rulesets frozen keeps those results meaningful.

Moving a ruleset through the lifecycle does not rewrite history. Past scan results keep the ruleset state they were run against.

## Why your ruleset vanished: the visibility filter

The rulesets table does not show archived rulesets by default. If a ruleset you expected to see is missing:

1. Open the rulesets table in the Cloud Manager.
2. Select **Edit filters** on the table.
3. Include **Archived** in the status filter.
4. Apply. The missing ruleset appears with Status **Archived**.

This is the single most common "where did my ruleset go" moment in governance administration, and the filter is the answer nine times out of ten.

## Restoring an archived ruleset

Restoring returns a ruleset to service in one step — Status goes straight back to **Published**, not to Draft:

1. Make archived rulesets visible (**Edit filters** → include **Archived**, as above).
2. Select the archived ruleset.
3. Use **Restore**.
4. Confirm the Status column returns to **Published**.

Because the restore path goes straight to Published, the ruleset is immediately back in force for new scans. If you wanted it back as a starting point for edits instead, restore it and then use **Save as new ruleset**.

## Editing a published ruleset: Save as new ruleset

Since published rulesets are immutable, the edit workflow is always versioning:

1. Select the published ruleset.
2. Use **Save as new ruleset**. This creates a new, editable version.
3. Make your changes and publish the new version.

Treat this as the routine maintenance path rather than an exception — any change to rules, filters, or metadata on a live ruleset goes through it.

## Archiving and deleting

**Archive** moves a published ruleset out of the way without destroying it. It disappears from the default table view, but it is restorable at any time.

**Delete** applies to archived rulesets and is irreversible. Before deleting, remember that historical scan results may still reference that ruleset — archive is reversible, delete is not. When in doubt, archive.

## Summary

Governance rulesets are Draft → Published → Archived, published rulesets are immutable, and edits always go through **Save as new ruleset**. Archived rulesets are hidden by the table's status filter — **Edit filters** → include **Archived** — and **Restore** brings one straight back to Published. Delete is permanent and only applies to archived rulesets; prefer archiving.

## Limitations and Notes

- Written against the 12.1.x lifecycle; UI labels can vary between versions, so check yours.
- This post covers the Cloud Manager UI path. If you need scripted lifecycle management, check the toolkit CLI's governance commands for your version.
- I have not walked every click-path on a live Cloud Manager for this one — the states, options, and behaviours are as the product documents them, but verify the exact placements on your own instance before relying on them in a change window.
