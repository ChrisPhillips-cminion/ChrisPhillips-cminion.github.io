---
layout: post
date: 2026-07-12 13:00:00
categories: APIConnect
title: "Dark Mode Support in IBM API Connect CMS Portal"
description: "How to enable and configure dark mode for custom themes in the IBM API Connect CMS Portal, including branding considerations and current limitations."
tags: [APIConnect, CMSPortal, DarkMode, Theming, DeveloperPortal]
draft: true
author: ["ChrisPhillips", "IBMBob"]
---

Dark mode support matters if your portal uses a custom theme and you want it to work well in both light and dark views. API Connect v12 adds dark-mode support to the CMS Portal theme system.

This article covers how dark mode works in the CMS Portal, how to configure it, and what to test.

<!--more-->

## Table of Contents

1. [What Dark Mode Means for CMS Portal Themes](#what-dark-mode-means-for-cms-portal-themes)
2. [How the Theme System Supports Dark Mode](#how-the-theme-system-supports-dark-mode)
3. [Enabling Dark Mode in Your Custom Theme](#enabling-dark-mode-in-your-custom-theme)
4. [Theme Variables for Light and Dark Modes](#theme-variables-for-light-and-dark-modes)
5. [Branding Considerations: Light + Dark](#branding-considerations-light--dark)
6. [Current Limitations](#current-limitations)
7. [Testing Your Dark Mode Theme](#testing-your-dark-mode-theme)

## What Dark Mode Means for CMS Portal Themes

The CMS Portal's theme system in v12 is built on a CSS custom properties (CSS variables) foundation. When dark mode is enabled, the portal switches to an alternate set of CSS variable values — colour palettes, backgrounds, borders, shadows — that are optimised for low-light environments.

This means:
- **Backgrounds shift** from white/light grey to dark grey/black
- **Text colours shift** from dark to light (with appropriate contrast ratios)
- **Accent colours** may shift slightly to maintain visibility against dark backgrounds
- **Icons and images** may need alternate versions for dark contexts

Importantly, dark mode is a **portal-level preference** — users can toggle it from their account menu, and the preference is persisted by the portal in the browser.

## How the Theme System Supports Dark Mode

The CMS Portal v12 theme uses a two-tier CSS variable system:

### Tier 1: Core Variables
These define the semantic meaning of a colour — e.g., `--color-text-primary`, `--color-background-surface`, `--color-border-default`. These are the variables your custom CSS should reference.

### Tier 2: Mode Tokens
These map semantic variables to actual colour values based on the active mode:

```css
/* Light mode (default) */
:root {
  --color-background-surface: #ffffff;
  --color-text-primary: #1a1a1a;
  --color-border-default: #e0e0e0;
  --color-accent-primary: #0052cc;
}

/* Dark mode */
[data-theme="dark"] {
  --color-background-surface: #1a1a2e;
  --color-text-primary: #e8e8e8;
  --color-border-default: #3a3a5c;
  --color-accent-primary: #4d9fff;
}
```

When you build a custom theme, you define the semantic variables. The mode tokens are applied automatically when dark mode is active.

## Enabling Dark Mode in Your Custom Theme

### Step 1: Enable Dark Mode in Theme Settings

In the CMS Portal admin:

1. Navigate to **Appearance** → **Themes** → **[Your Custom Theme]**
2. Find the **Colour Scheme** section
3. Toggle **Enable Dark Mode** to on
4. Save

A theme with dark mode enabled should expose separate settings for the dark palette alongside the light palette.

### Step 2: Define Dark Mode Colour Overrides

Once enabled, additional colour fields appear in your theme settings for dark mode. These mirror the light mode fields but are specifically for the dark palette:

| Setting | Light Mode Default | Dark Mode Recommended |
|---|---|---|
| Background | #ffffff | #1a1a2e |
| Surface | #f5f5f5 | #252542 |
| Text Primary | #1a1a1a | #e8e8e8 |
| Text Secondary | #666666 | #a0a0b0 |
| Accent Primary | #0052cc | #4d9fff |
| Accent Hover | #003d99 | #80b5ff |
| Border | #e0e0e0 | #3a3a5c |
| Error | #b71c1c | #ff6b6b |
| Success | #1b5e20 | #69db7c |

### Step 3: Apply to Your Theme CSS

In your custom theme's `styles.css`, use semantic variables rather than hardcoded colours:

```css
/* ✅ Good: uses semantic variables */
.my-card {
  background-color: var(--color-background-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
}

/* ❌ Bad: hardcoded colour */
.my-card {
  background-color: #ffffff;
  color: #1a1a1a;
}
```

By using semantic variables throughout your custom CSS, dark mode support comes "for free" — you only need to set the dark mode colour values in the theme settings, and all your components automatically adapt.

## Theme Variables for Light and Dark Modes

Here's a comprehensive reference of the key CSS variables you'll use in custom CMS Portal themes:

```css
/* Background layers */
--color-background-base       /* Lowest layer, page background */
--color-background-surface    /* Cards, panels, elevated surfaces */
--color-background-overlay    /* Modals, dropdowns, popovers */

/* Text */
--color-text-primary         /* Headings, primary content */
--color-text-secondary       /* Descriptions, labels */
--color-text-disabled        /* Disabled state text */
--color-text-inverse         /* Text on dark/accent backgrounds */

/* Borders */
--color-border-default       /* Standard borders */
--color-border-strong        /* Emphasised borders */
--color-border-focus         /* Focus rings, :focus-visible */

/* Accent / Brand */
--color-accent-primary       /* Primary buttons, links */
--color-accent-hover         /* Hover state */
--color-accent-pressed       /* Active/pressed state */

/* Semantic */
--color-error:               /* Error states */
--color-warning:             /* Warning states */
--color-success:             /* Success states */
--color-info:                /* Informational states */

/* Code */
--color-code-background:      /* Inline code backgrounds */
--color-code-text:            /* Inline code text */
```

## Branding Considerations: Light + Dark

When designing your dark mode palette, keep these branding considerations in mind:

### 1. Your Brand Colours May Need Adjustment
Your primary brand colour (e.g., a navy blue) might look stunning on a white background but disappear against a dark background. Test your accent colours against both backgrounds and adjust if necessary. A common approach is to **lighten brand colours for dark mode** — instead of `#0052cc`, use `#4d9fff`.

### 2. Logos
If your logo has a dark version for use on light backgrounds, you likely also need a light version for dark mode. Use the CSS `data-theme` attribute to swap logos:

```css
/* In your theme's logo CSS */
.site-logo {
  content: url('/images/logo-light.png');
}

[data-theme="dark"] .site-logo {
  content: url('/images/logo-dark.png');
}
```

### 3. Screenshots and Images in Content
CMS-managed content pages (guides, tutorials) may contain embedded images with light backgrounds. The portal doesn't automatically invert these. Consider adding a CSS filter for dark mode:

```css
[data-theme="dark"] .content-body img:not([src*="dark"]) {
  filter: brightness(0.85) contrast(1.1);
}
```

> **Note**: This is a global filter and may not suit all images. Test carefully.

### 4. API Documentation Code Samples
Code samples in your API documentation typically have dark backgrounds in most developer tools. Make sure your docs theme supports dark mode code blocks — this is likely the highest-impact dark mode improvement for developer experience.

## Current Limitations

Be aware of these known limitations in v12.1.1 dark mode:

- **Not all CMS components are dark-mode aware**: Some older portal components (particularly in legacy admin sections) may not yet respond to the theme. Test thoroughly.
- **Custom JavaScript**: If your theme includes custom JavaScript that injects HTML with hardcoded styles, those won't respond to dark mode. Audit any inline styles in custom JS.
- **User preference detection**: The portal respects `prefers-color-scheme` from the OS/browser when a user first visits, but doesn't auto-update if the OS preference changes mid-session without a page reload.
- **PDF exports**: If your portal generates PDF exports of documentation, these are currently always rendered in light mode.
- **Third-party embeds**: Any third-party iframes or embeds (e.g., embedded Swagger UI, external widgets) are not affected by the CMS dark mode setting.

Check the IBM documentation for your exact API Connect version to confirm the current list of dark mode limitations and supported theme capabilities.

## Testing Your Dark Mode Theme

Test your dark mode theme thoroughly across:

1. **Toggle test**: Switch dark mode on and off in the portal and verify all major pages (home, API listing, API detail, documentation, subscription wizard) adapt correctly.
2. **Accessibility**: Run both light and dark modes through a contrast checker (e.g., WebAIM Contrast Checker). Minimum WCAG AA requires 4.5:1 for normal text.
3. **All major browsers**: Chrome, Firefox, Safari, Edge — both light and dark mode.
4. **Mobile**: Test dark mode on both iOS Safari and Android Chrome, which have their own dark mode rendering modes that can interact with the portal's CSS.
5. **Screenshot diff**: Capture before/after screenshots of each major page in both modes for your design review.

## Summary

Dark mode support in the CMS Portal is a meaningful quality-of-life improvement for your developer community. By building your custom theme on semantic CSS variables from the start, dark mode support becomes nearly automatic — you just need to define the dark palette alongside your light palette.

Invest the time to test it properly, especially around accessibility contrast ratios. A poorly implemented dark mode that's hard to read is worse than no dark mode at all.
