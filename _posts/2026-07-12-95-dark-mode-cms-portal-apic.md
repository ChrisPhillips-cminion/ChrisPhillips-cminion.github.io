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

Dark mode support matters if your portal uses a custom theme and you want it to work well for developers who prefer dark views. API Connect v12 adds dark-mode support to the CMS Portal theme system.

<!--more-->

## How the Theme System Supports Dark Mode

The CMS Portal v12 theme uses a two-tier CSS variable system:

**Tier 1: Core Variables** — semantic meanings such as `--color-text-primary`, `--color-background-surface`, `--color-border-default`. Your custom CSS should reference these.

**Tier 2: Mode Tokens** — map semantic variables to actual colour values based on the active mode:

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

Dark mode is a **portal-level preference** — users toggle it from their account menu and the preference is persisted by the portal.

## Enabling Dark Mode in Your Custom Theme

### Step 1: Enable Dark Mode in Theme Settings

1. Navigate to **Appearance** → **Themes** → **[Your Custom Theme]**
2. Find the **Colour Scheme** section
3. Toggle **Enable Dark Mode** to on
4. Save

### Step 2: Define Dark Mode Colour Overrides

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

Use semantic variables throughout your custom CSS:

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

By using semantic variables, dark mode support comes free — you only need to set the dark palette values in theme settings and all components adapt.

## Theme Variables Reference

```css
/* Background layers */
--color-background-base       /* Page background */
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
--color-border-focus         /* Focus rings */

/* Accent / Brand */
--color-accent-primary       /* Primary buttons, links */
--color-accent-hover         /* Hover state */
--color-accent-pressed       /* Active/pressed state */

/* Semantic */
--color-error
--color-warning
--color-success
--color-info

/* Code */
--color-code-background
--color-code-text
```

## Branding Considerations

**Brand colours may need adjustment.** A navy blue that looks great on white may disappear against a dark background. A common approach is to lighten brand colours for dark mode — instead of `#0052cc`, use `#4d9fff`.

**Logos.** If your logo has a dark version for use on light backgrounds, you likely also need a light version for dark mode:

```css
.site-logo {
  content: url('/images/logo-light.png');
}

[data-theme="dark"] .site-logo {
  content: url('/images/logo-dark.png');
}
```

**Screenshots and images in content.** CMS-managed content pages may contain embedded images with light backgrounds. The portal doesn't automatically invert these:

```css
[data-theme="dark"] .content-body img:not([src*="dark"]) {
  filter: brightness(0.85) contrast(1.1);
}
```

> **Note:** This is a global filter and may not suit all images. Test carefully.

**API documentation code samples.** Code samples in API documentation typically have dark backgrounds in most developer tools. Ensure your docs theme supports dark mode code blocks — this is the highest-impact dark mode improvement for developer experience.

## Limitations and Notes

- **Not all CMS components are dark-mode aware.** Some older portal components (particularly in legacy admin sections) may not yet respond to the theme.
- **Custom JavaScript.** If your theme injects HTML with hardcoded styles, those won't respond to dark mode. Audit any inline styles in custom JS.
- **User preference detection.** The portal respects `prefers-color-scheme` from the OS/browser when a user first visits, but doesn't auto-update if the OS preference changes mid-session without a page reload.
- **PDF exports** are currently always rendered in light mode.
- **Third-party embeds** are not affected by the CMS dark mode setting.

Check the IBM documentation for your exact API Connect version for the current list of supported theme capabilities.

## Testing Your Dark Mode Theme

1. **Toggle test:** Switch dark mode on and off and verify all major pages adapt correctly (home, API listing, API detail, documentation, subscription wizard)
2. **Accessibility:** Run both modes through a contrast checker. Minimum WCAG AA requires 4.5:1 for normal text
3. **All major browsers:** Chrome, Firefox, Safari, Edge — both light and dark
4. **Mobile:** Test on iOS Safari and Android Chrome
5. **Screenshot diff:** Capture before/after screenshots of each major page in both modes for design review
