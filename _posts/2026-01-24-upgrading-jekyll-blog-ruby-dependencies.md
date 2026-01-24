---
layout: post
date: 2026-01-24 17:48:00
categories: Jekyll
title: "Upgrading a Jekyll Blog: Managing Ruby Versions and Dependencies"
author: ["ChrisPhillips"]
image: /images/2026-01-24-jekyll-upgrade.png
description: "A practical guide to upgrading Jekyll and Ruby dependencies for a GitHub Pages blog, including troubleshooting rbenv and bundler issues."
tags: [Jekyll, Ruby, rbenv, Bundler, GitHub Pages, Blog, DevOps, Upgrade]
draft: true
---

I'll be the first to admit it: I wasn't practicing what I preach. For someone who regularly writes about best practices, and keeping systems up to date, I had let my own Jekyll blog fall embarrassingly behind. My Jekyll version was ancient, my Ruby dependencies were outdated, and I had been ignoring the problem for far too long.

This is terrible. Not just because outdated software can have security vulnerabilities, but because it goes against everything I advocate for in my professional work. If I'm going to write about proper software maintenance and infrastructure management, I need to walk the walk.

So today, I decided enough was enough and (with a daughter asleep on top of me) it was time to update my blog's Jekyll installation and get everything current. What followed was a journey through Ruby version management, dependency resolution, and the occasional head-scratching moment that reminded me why keeping things updated regularly is so much easier than letting them fall behind.

Here's what I learned (well, re-learned) during the process.

<!--more-->

## The Challenge: Ruby Version Management

When upgrading a Jekyll blog, one of the first challenges is ensuring you have the correct Ruby version installed. My blog required Ruby 3.3.10, but I initially had Ruby 3.3.0 installed via rbenv.

### Installing the Correct Ruby Version

Using rbenv, I started the installation process:

```bash
rbenv install 3.3.10
```

This process takes several minutes as it compiles Ruby from source. While waiting for the installation to complete, I discovered that Ruby 3.3.0 was already available and could be used temporarily since both are 3.3.x versions.

### The rbenv Path Issue

A common issue when working with rbenv is ensuring the shell properly initializes it. Simply running commands may use the system Ruby instead of the rbenv-managed version. The solution is to explicitly initialize rbenv in your command:

```bash
eval "$(rbenv init - bash)" && rbenv shell 3.3.0
```

This ensures that:
1. rbenv is properly initialized in the current shell
2. The correct Ruby version is activated
3. All subsequent commands use the rbenv-managed Ruby

## Installing Dependencies with Bundler

Once Ruby was properly configured, the next step was installing the project dependencies.

### Installing Bundler

First, I needed to install Bundler itself:

```bash
gem install bundler
```

### Installing Project Dependencies

With Bundler installed, I could install all the Jekyll dependencies specified in the Gemfile:

```bash
bundle install
```

This installed Jekyll 4.4.1 along with all required plugins and dependencies:
- jekyll-archives
- jekyll-feed
- jekyll-remote-theme
- jekyll-seo-tag
- jekyll-sitemap
- jekyll-paginate
- jekyll-commonmark
- jekyll-include-cache
- kramdown-parser-gfm
- liquid-c (for performance)
- webrick (required for Ruby 3.0+)

## Running Jekyll Locally

With all dependencies installed, starting the local development server was straightforward:

```bash
bundle exec jekyll serve
```

The server started successfully and was accessible at `http://127.0.0.1:4000/`. The key features enabled:
- **Auto-regeneration**: Changes to files automatically rebuild the site
- **Local preview**: Full site functionality available for testing
- **Fast iteration**: Make changes and see results immediately

## Key Takeaways

### 1. Use rbenv for Ruby Version Management

rbenv provides clean, isolated Ruby environments. Always ensure it's properly initialized:

```bash
eval "$(rbenv init - bash)"
```

### 2. Bundle Exec is Essential

Always run Jekyll commands with `bundle exec` to ensure you're using the correct gem versions:

```bash
bundle exec jekyll serve
```

### 3. Ruby 3.0+ Requires webrick

Modern Ruby versions (3.0+) no longer include webrick by default. Ensure it's in your Gemfile:

```ruby
gem "webrick", "~> 1.8"
```

### 4. Version Compatibility Matters

While Ruby 3.3.0 and 3.3.10 are both 3.3.x versions and generally compatible, it's best practice to use the exact version specified in `.ruby-version` for production deployments.

## Useful Commands Reference

```bash
# Check installed Ruby versions
rbenv versions

# Install a specific Ruby version
rbenv install 3.3.10

# Set local Ruby version for a project
rbenv local 3.3.10

# Check Jekyll version
bundle exec jekyll --version

# Serve with live reload
bundle exec jekyll serve --livereload

# Serve including draft posts
bundle exec jekyll serve --drafts

# Serve with incremental builds (faster)
bundle exec jekyll serve --incremental
```

## Conclusion

Upgrading a Jekyll blog requires careful attention to Ruby version management and dependency installation. By using rbenv for Ruby version management and bundler for dependency management, you can maintain a clean, reproducible development environment. The key is ensuring all tools are properly initialized and using `bundle exec` to run Jekyll commands with the correct gem versions.

The entire upgrade process—from installing Ruby to running the local server—can be completed in under 10 minutes once you understand the workflow. With auto-regeneration enabled, you can immediately start developing and testing changes locally before deploying to production.