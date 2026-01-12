---
layout: post
date: 2026-01-12 11:00:00
categories: DevOps
title: "Terraform: An Excellent Infrastructure Tool, But Not for API Deployments"
draft: true
---

Terraform is an excellent tool for managing infrastructure. I use it, I recommend it, and I've seen it work brilliantly in production environments. However, I've also seen teams try to force it into application deployment scenarios where it simply doesn't belong. This article explains why Terraform should stay in its lane - infrastructure - and why your APIs deserve better.

<!--more-->

## Section 1: Why Terraform is Great for Infrastructure

Terraform excels at provisioning infrastructure. Need to spin up VMs, configure networks, set up load balancers, or manage DNS? Terraform is your friend. The declarative approach works perfectly for infrastructure because:

**Infrastructure changes infrequently.** Once you've provisioned a VM or configured a network, it stays that way for weeks or months. Terraform's state management makes sense here - it accurately tracks what exists and what needs changing.

**Idempotency is natural.** Run the same Terraform config ten times, get the same result. Perfect for infrastructure.

**Multi-cloud support.** Terraform abstracts away provider differences, letting you manage AWS, Azure, and on-prem resources with the same tooling.

## Section 2: The Application Deployment Problem

Applications are not infrastructure. They change multiple times per day. They need rolling updates, health checks, and rollback procedures. They require orchestration that Terraform was never designed to provide.

### Frequent Changes Break Terraform's Model

In a modern DevOps environment, applications deploy constantly. Each deployment involves:
- Rolling updates across multiple instances
- Database migrations
- Cache invalidation
- Health checks and rollback procedures

Terraform's state file becomes a bottleneck. The risk of state corruption increases with each deployment. You're fighting the tool rather than working with it.

### Deployment Orchestration

Application deployments need sophisticated orchestration:
- Blue-green deployments
- Canary releases
- A/B testing
- Traffic splitting

Can you force Terraform to do these? Sure. Should you? Absolutely not.

### Lifecycle Management

When you deploy a new application version, you don't destroy and recreate resources - you update them in place with zero downtime. Terraform's create-update-destroy model doesn't fit this pattern.

## Section 3: Use the Right Tool

For application deployments, use tools designed for the job:

- **ArgoCD** or **FluxCD** for GitOps
- **Ansible** for configuration management
- **CI/CD pipelines** (Jenkins, GitLab CI, GitHub Actions) for orchestration

These tools understand application deployment patterns. They provide rolling updates, health checks, traffic management, and integration with monitoring systems.

## Section 4: The Grey Area: When APIs Become Infrastructure

There's an edge case worth discussing: APIs that function as infrastructure.

Consider an API that:
- Provides core infrastructure services (authentication, service mesh, API gateway)
- Changes quarterly or less
- Has no complex deployment orchestration
- Is treated as a foundational platform component

In this specific case, Terraform might be appropriate. But this is uncommon.

### When an API Qualifies as Infrastructure

An API might be infrastructure if it meets ALL these criteria:

1. **Stability** - Changes less than quarterly
2. **Foundational** - Other services depend on it as a platform
3. **Simple deployment** - No complex orchestration needed
4. **Stateless or externally managed state** - Doesn't manage critical application state
5. **Infrastructure-like lifecycle** - Provisioned once, rarely updated
6. **Ownership** - Managed by infrastructure teams, not application teams

Even then, think carefully. A dedicated application deployment tool might still be better.



## Section 5: In Summary

Terraform is excellent for infrastructure. Use it to provision VMs, networks, load balancers, and storage. But don't use it for application deployments.

Applications need tools that understand deployment patterns, orchestration, and rapid change cycles. While rare cases exist where an API might be considered infrastructure, these are uncommon and need careful evaluation.

**Use the right tool for the right job.** Provision infrastructure with Terraform. Deploy applications with tools designed for that purpose.

### Further Reading:
- [Pipelines :: How and why to use them to deploy Products and APIs into API Connect](https://chrisphillips-cminion.github.io/apiconnect/2020/09/18/pipelines.html)
- [101 Rules for Deploying with Dev Ops](https://chrisphillips-cminion.github.io/misc/2019/06/20/DevOpsRules.html)