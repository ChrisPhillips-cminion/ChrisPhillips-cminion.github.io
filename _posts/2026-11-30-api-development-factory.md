---
layout: post
date: 2026-11-30 09:00:00
categories: APIConnect
title: "Building an API Development Factory: Scaling API Delivery with Governance, Automation, and Reusable Patterns"
author: ["ChrisPhillips"]
description: "How enterprises move from bespoke API projects to an industrialised delivery model — the three operating models (simple form, template-based, free-form), the automation that powers them, and why most mature enterprises standardise on a template-based factory."
tags: [APIConnect, PlatformEngineering, APIGovernance, Automation, CICD, Architecture]
draft: true
image: /images/api-development-factory.png
---

Every successful API programme eventually hits the same wall, and it is not a technology wall. The delivery model that produced the first fifty APIs — a project team, a bespoke design, a careful manual deployment — cannot produce the next five hundred. Demand outgrows the central team, quality varies with whoever built each API, and governance turns into a queue. The programme praised for agility is now criticised for bottlenecks.

The organisations that get through this wall do not work harder at the old model. They change the model. This article is about that change: the API development factory, the operating models that implement it, and the trade-offs between them.

<!--more-->

## The bespoke ceiling

Building every API as a bespoke project works brilliantly at small scale and fails predictably at large scale. Each API becomes a snowflake: its own design conventions, security configuration, deployment ritual, and documentation style — held together by tribal knowledge.

The costs compound quietly. Review effort grows linearly with API count because nothing is ever the same twice. Reuse does not happen because nobody can find what already exists. Security posture depends on which team built the API and in which year. And the centre — the team expected to hold all this together — becomes the constraint on everyone's delivery.

The bespoke model does not fail because people are doing bad work. It fails because it asks people to repeatedly solve problems that were already solved.

## What an API development factory is

A factory is industrialised delivery: standard parts, automated assembly, and quality control built into the line rather than inspected at the end. Applied to APIs, that means approved templates and reusable patterns instead of blank pages; automated validation and deployment pipelines instead of manual checklists; and governance encoded into the tooling instead of enforced in meetings.

A factory removes toil — the repetitive, error-prone, no-judgement-required work — so that engineering attention goes where it belongs: the business logic, the data model, the consumer experience. No automotive engineer laments no longer hand-tightening every bolt.

## The platform engineering foundation

Underneath the factory is platform engineering, and the disciplines that come with it: **golden paths** — the well-lit, supported route from code to production; **paved-road architectures** — the standard building blocks a team assembles rather than invents; and **self-service enablement** — the ability for a product team to design, build, validate, and deploy an API without filing a ticket or waiting for a central team's calendar.

The platform team treats this capability as a product, with users, roadmap, and feedback loop. Their success metric is brutal and clarifying: how much must a team know, and how many people must they ask, to deliver a compliant, secure, supported API to production? When that approaches zero, the factory is working.

## Three operating models

Enterprises implement the factory in three broad shapes. Each is legitimate. Each has consequences.

### 1. The simple form model

Teams request APIs through a controlled intake process; a central operations team owns the standards, the build, and the deployment.

- **Advantages:** the highest consistency and governance of the three. Standards are applied by the people who wrote them; security is uniform because few hands configure anything.
- **Risks:** throughput is capped by the central team's capacity, and the cap is felt organisation-wide. Delivery dates drift from the consumers' needs to the centre's queue. Teams disengage — if the centre owns the outcome, the centre gets the care.
- **Suitable organisations:** small estates, early-maturity programmes, or tightly regulated contexts where one control point outweighs speed.
- **Governance implications:** governance concentrates at intake — a gate by design, effective but unable to scale past the queue.
- **Operational considerations:** the central team scales linearly with demand, which is to say badly. Every new API adds permanent load.
- **Security considerations:** strong and consistent, but change is slow — including the response to a new threat.

I watched a bank run this model into the ground at around two hundred APIs: a twelve-week intake queue, and a shadow estate growing because the official path was slow. The model did not fail at governance. It failed at absorption.

### 2. The template-based factory

Teams build from approved templates and reusable patterns, through automated validation and deployment pipelines they run themselves.

- **Advantages:** the best balance of control and agility. Standards are embedded in the starting point, so compliance is the default. Reuse compounds — every pattern hardened once is inherited by every subsequent API. Delivery pace is set by product teams, not by a queue.
- **Risks:** template sprawl — dozens of overlapping templates, each with a constituency — and template decay, where the paved road lags behind platform changes and teams start forking. Templates themselves become products needing owners, roadmaps, and deprecation policies.
- **Suitable organisations:** most enterprises — especially regulated industries, where auditors want consistency at the pace delivery teams demand. Effective from roughly fifty APIs into the thousands.
- **Governance implications:** governance shifts into the templates and pipelines — [guardrails rather than gates]({% link _posts/2026-11-29-api-governance-enabling-scale.md %}). The governance surface becomes small and strategic: what the templates must enforce, which exceptions are permitted.
- **Operational considerations:** the platform team's workload moves from building APIs to building and maintaining the factory. Onboarding is fast because knowledge is encoded, not oral.
- **Security considerations:** security is baked into the template and enforced in the pipeline, so the baseline is uniform by construction. Exceptions are explicit, visible, and reviewable — and can carry expiry dates.

This is the model I recommend to most enterprises, and the one that carried an insurer past four hundred APIs with a two-person platform team and a median design-to-production time in days. The [decentralised-team factory pattern]({% link _posts/2020-08-26-APIGov2.md %}) covers the same questions I faced scaling delivery.

### 3. The free-form factory

Teams have maximum autonomy: any design, any pattern, their own pipelines — with validation happening during pipeline execution rather than before it.

- **Advantages:** the fastest innovation of the three. Strong teams move without coordination cost, and the model attracts engineers who value autonomy.
- **Risks:** drift is structural, not exceptional. Every incident is an archaeology exercise, because nothing is standard. Support costs scale with variety.
- **Suitable organisations:** high-trust, high-discipline engineering cultures — typically digital natives with strong platform maturity and an appetite for owning consequences.
- **Governance implications:** governance must be entirely policy-as-code, because there is no earlier checkpoint. If a rule is not automated, it is not a rule.
- **Operational considerations:** demands the most mature observability and platform engineering. You are choosing to govern at runtime; you had better be excellent at runtime.
- **Security considerations:** only as strong as the automated checks and the exceptions you can detect. Blast radius is larger because variance is larger.

| | Simple form | Template-based | Free-form |
|---|---|---|---|
| Consistency | Highest | High | Variable |
| Delivery speed | Queue-limited | Team-limited | Fastest |
| Scaling behaviour | Linear (poor) | Compounding | Compounding, with drift |
| Governance style | Gate | Guardrails | Runtime policy |
| Operational load | Central team | Platform team | Everyone |
| Security baseline | Uniform, slow to change | Uniform by construction | As good as the checks |

## The production line: CI/CD and automation

Whatever the model, the factory runs on the same machinery:

- **Git repositories** hold API definitions, templates, and policies as versioned, reviewed, auditable artifacts. The repository is the system of record, not anyone's laptop.
- **API templates and reusable patterns** are the standard parts: a team starts from an approved, already-compliant baseline instead of a blank file.
- **Automated testing** — contract tests, functional tests, and security scanning — runs on every change. [Linting the definition itself]({% link _posts/2020-09-28-apicgov3-linting.md %}) catches the cheap errors before they become expensive ones.
- **Policy validation** checks the API against the organisation's rules — naming, versioning, authentication, documentation — as a pipeline stage, not a review meeting.
- **Deployment pipelines** promote the API through environments on merge, [publishing products into API Connect from the pipeline]({% link _posts/2020-09-18-pipelines.md %}) rather than by hand. If deployment needs a human clicking through a console, it is not a factory yet.

Each automated check is a class of defect that stops existing, permanently.

## IBM API Connect as the runtime and governance layer

A factory needs somewhere for its output to run. In a factory architecture, IBM API Connect plays the runtime and governance layer: the gateway enforces security and usage policy identically regardless of which team produced the API; the catalogue is the storefront where published APIs are discovered, with lifecycle states that make deprecation and retirement visible rather than folkloric; and the analytics — usage, errors, latency, per consumer — feed the factory's quality loop, telling you which APIs are earning their keep.

The strategic point: publication becomes a pipeline product. The API definition moves through Git, validation, and promotion, and lands in the runtime without a human in the loop — with governance enforced at the gateway, so security posture does not depend on which team shipped. [Governance as code]({% link _posts/2020-10-26-apicgov4-as-code.md %}) and [a working rule set]({% link _posts/2024-04-05-gov-apic-gp.md %}) make the policy layer versioned and reviewable.

## Policy as code and shift-left governance

The unifying discipline across all three models is policy as code: the organisation's rules — security baselines, naming, versioning, documentation — expressed as versioned, automatically-enforced checks rather than documents and meetings.

That is what makes shift-left governance real: a developer learns about a standards violation at commit time, in seconds — not at a review board three weeks later. The fix is cheaper, and the board's remaining agenda shrinks to the questions that genuinely need human judgement.

## Starting small and evolving

You do not build a factory in one programme:

1. **Start with one template and one pipeline.** Pick the most common API shape in your estate — almost certainly REST-over-gateway-to-backend — and pave that one road end to end.
2. **Measure it.** Time from design to production, defect rates, adoption of the template versus the old way. Evidence, not enthusiasm, funds the next step.
3. **Grow the pattern library from repetition, not speculation.** Add a template when a third team solves the same problem a third time.
4. **Let the operating model mature with the estate.** Many organisations begin in simple-form mode, adopt the template-based factory as demand outgrows the queue, and only the rare few relax toward free-form.

## Executive recommendations

1. **Default to the template-based factory.** For most enterprises it delivers governance and speed together; the other two models are special cases.
2. **Fund the platform team as a product team.** The factory's throughput, security, and reliability are their product. Staff and measure them accordingly.
3. **Give every template an owner and a lifecycle.** Template sprawl and decay are the failure modes; ownership is the countermeasure.
4. **Automate every objective check.** Any rule a machine can enforce should be; reserve human review for duplicate-risk and exception decisions.
5. **Track delivery and governance metrics together** — lead time and compliance rate on the same dashboard. The factory's promise is that they improve together.
6. **Start with one golden path this quarter.** A single paved road, end to end, beats a strategy document.

## Conclusion: standard parts, differentiated products

Mature enterprises converge on the template-based factory for a reason manufacturing worked out a century ago: standardise the parts and the process, so the differentiation goes into the product. Teams should not spend creativity on how to secure a gateway or which versioning scheme to use — those questions have answers, and the answers belong in the pavement. Creativity belongs in the business capability the API exists to expose.

Start with one template, one pipeline, and the discipline to measure the result. The day a team ships a compliant, secure, supported API to production without asking anyone's permission is the day you know you have built a factory.
