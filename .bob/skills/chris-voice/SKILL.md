---
name: chris-voice
description: Use when editing, reviewing, or rewriting a blog post to match Chris Phillips' writing voice and style. Activate when the user asks whether a post sounds like them, wants it rewritten in their style, or wants AI-sounding content removed.
---

# Chris Phillips Voice Guide

When editing or rewriting a blog post for Chris Phillips, apply every rule below. The goal is to make the post sound like a working IBM API Connect/DataPower specialist wrote it on a Friday afternoon — not like a product documentation team.

---

## Core Principles

**1. Get in, say the thing, get out.**
Chris writes short. No preamble, no throat-clearing, no "In this article we will explore…". If a sentence restates what the heading already says, delete it.

**2. One strong opening sentence — not a mission statement.**
The first sentence either states a concrete problem ("When X happens, Y breaks") or opens with a real-world incident/observation. Never start with a generic definition or a list of what the article covers.

**3. No Table of Contents for short or medium posts.**
Only add a ToC if the article is genuinely long (7+ substantive sections). Most posts don't need one.

**4. No "Best Practices" sections.**
Chris never has a stand-alone best-practices section. If there are recommendations, they appear inline, at the moment they're relevant — not collected into a generic call-out at the end.

**5. No motivational closing.**
Delete any closing sentence that could appear on a motivational poster. Examples of things to cut:
- "The time you invest in X will save you Y later."
- "Don't skip this step."
- "With the right approach, you can achieve Z."
The last sentence of a post should be a concrete fact, a next-step pointer, or nothing.

**6. Keep `## Summary` and `## Limitations and Notes` — but make them concise.**
These sections are valid and should be retained. A `## Summary` should add something: a synthesis, a recommendation, or a forward pointer — not just a bullet-point recap of headings. A `## Limitations and Notes` section is useful for version requirements, caveats, and "not a real-time tool" style warnings. Keep both tight — no padding, no repetition of what the body already said.

---

## Voice and Tone

**Direct, not diplomatic.** Chris states opinions plainly: "I would go with Option 1." Not "You may wish to consider Option 1 depending on your requirements."

**British English.** organisation (not organization), behaviour, favour. Use `<!--more-->` for the fold, not `<!-- more -->`.

**No hedging.** Phrases like "or similar, depending on your version" and "you may wish to" weaken the post. Either state the fact confidently or leave it out.

**Short sentences.** If a sentence has more than two clauses, split it. This isn't academic writing.

**Plain transitions.** "Here is X." "This does Y." Not "In order to understand X, it is important to first appreciate that Y..."

**Personal but not chatty.** Chris says "I" when giving a personal recommendation ("My opinion: Option 1"). He doesn't do cheerful filler ("Great question!", "Let's dive in!").

**No emojis. No decorative callout boxes.** Use `>` blockquotes only for genuine warnings or version-specific notes, not for emphasis.

---

## Structural Patterns

### Opening
- Incident-driven: real scenario from the field that motivates the article.
- Or: direct statement of the problem the article solves.
- Or (for short how-to posts): one-sentence context + `<!--more-->`.

### Body
- Numbered steps for procedures (`### Step 1: ...`)
- Prose for concepts and diagnosis
- Code blocks for every command — no paraphrasing shell commands in prose
- Inline comments in code (`# what this does`) are fine; verbose code preambles are not

### Closing
- Link to the next article in a series using the pattern at the bottom of longer posts: `*Next: "Title" — short description.*`
- Or nothing. An abrupt end is fine.
- A `## Summary` is fine if it adds synthesis or a forward pointer. Cut it only if it's a pure restatement of headings.

---

## Frontmatter

Correct frontmatter for a standard post:

```yaml
---
layout: post
date: YYYY-MM-DD HH:MM:SS
categories: APIConnect
title: "Title here"
---
```

Always preserve `description:`, `tags:`, and `author:` if they are present in the original file. Do not remove them.

For `author:`, Chris uses `["ChrisPhillips"]` for solo posts and `["ChrisPhillips", "co-author"]` for joint posts.

---

## Red Flags to Remove

When reviewing a post, flag and fix all of the following:

| Anti-pattern | Fix |
|---|---|
| `## Table of Contents` on a short post | Delete it |
| `## Best Practices` section | Fold content inline or cut |
| `## Summary` that only restates headings | Rewrite to add synthesis or a forward pointer |
| `## Limitations and Notes` padded with filler | Tighten to a bullet list of genuine caveats |
| "In this article we will cover..." | Delete the sentence |
| "This is useful for...", "This is important because..." | Get to the point instead |
| Closing motivational sentence | Delete it |
| "or similar, depending on your version" | Either state the correct value or cut |
| Bullet lists that repeat what the section heading says | Merge or cut |
| 3+ clauses in one sentence | Split it |
| "You should consider..." | "Consider..." or just state the rule |
| Hedged instructions ("you may wish to") | Make them direct ("do this") |

---

## What Makes a Chris Phillips Post Feel Right

The Backup/DR post and the Gateway Re-registration post are good examples of the newer style. They:
- Open with a real incident or concrete failure scenario
- Diagnose in numbered steps with actual commands
- State opinions plainly ("Monitor the webhook state — is worth months of incident-free publishing")
- End with a `*Next:*` pointer or nothing

The SSL Certificates post and the API Gateway Location post are good examples of the older, shorter style. They:
- State the thing in one sentence
- Get straight into the numbered list or pros/cons
- End without ceremony

Both styles are valid. The key is: every sentence earns its place.

---

## When Rewriting

1. Read the whole post first before changing anything.
2. Check the opening — if it doesn't grab, rewrite it. One strong sentence.
3. Cut Table of Contents and Best Practices sections. Keep Summary and Limitations — tighten them if needed.
4. Find every hedged/weak sentence and make it direct or cut it.
5. Find the closing motivational sentence and delete it.
6. Check British spelling throughout.
7. Read aloud. If it sounds like a product brochure, rewrite that paragraph.
8. Do not add new sections or information that wasn't in the original post.
