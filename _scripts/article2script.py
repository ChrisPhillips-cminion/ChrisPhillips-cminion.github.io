#!/usr/bin/env python3
"""
article2script.py — turn a blog post into an informal spoken-word script.

Calls an OpenAI-compatible /chat/completions endpoint to rewrite a markdown
post as a conversational script the author can record (or feed to a voice
clone). The script text is written to _audio/ (an underscore directory, so
Jekyll never publishes it).

Environment:
  LLM_BASE_URL   base URL of the endpoint, up to but not including
                 /chat/completions (e.g. https://host/v1)
  LLM_API_KEY    sent as "Authorization: Bearer <key>" (omit if none needed)
  LLM_MODEL      default model (overridable with --model)

Usage:
  python3 _scripts/article2script.py --list-models
  python3 _scripts/article2script.py _posts/2026-11-29-api-governance-enabling-scale.md
  python3 _scripts/article2script.py _posts/2026-11-30-api-development-factory.md \
      --model glm-5-3 --out _audio/factory-test.md
  python3 _scripts/article2script.py _posts/2026-11-29-api-governance-enabling-scale.md \
      --dry-run        # show the prompt without calling the API

Stdlib only — no pip installs needed.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

WPM = 150  # spoken words per minute, for runtime estimates
DEFAULT_MODEL = "granite-5-0-230b-preview-r261008a"

SYSTEM_PROMPT = """\
You turn technical blog articles into spoken-word scripts for the author to \
record as audio.

The author is a British enterprise integration architect. The script must \
sound like him talking informally to a colleague down the pub: knowledgeable, \
opinionated, dry humour, never lecturing, never reading from a page.

Hard rules:
- Write for the ear: short sentences, contractions, direct address \
("you know how it goes").
- Output flowing spoken paragraphs only. No headings, no bullet points, \
no tables, no markdown syntax of any kind.
- Keep every argument, anecdote, number and recommendation from the article. \
Add nothing: no new facts, no new examples, no new numbers.
- Where the article uses a list or a table, talk through the points \
conversationally instead of enumerating them mechanically.
- Keep the author's first-person anecdotes in the first person.
- British English spelling and idiom.
- Open with a conversational hook that restates the article's opening idea. \
End with the article's conclusion as a parting thought.
- Separate paragraphs where the speaker should breathe. Use [pause] only for \
a deliberate dramatic stop, not as ordinary punctuation.
- Output only the script text: no preamble, no title, no closing notes.
"""


def strip_markdown(text: str) -> str:
    """Reduce a Jekyll post to plain text the model can rewrite."""
    # YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    # HTML comments (incl. <!--more-->)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    # images
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # markdown links -> link text only (handles {% link %} inside the parens)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # any leftover liquid tags
    text = re.sub(r"\{%-?\s*\w+[^%]*%\}", "", text)
    # inline code, bold, italic markers
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", text)
    # headings -> SECTION markers (structure hint for the model, not output)
    text = re.sub(r"^#{1,6}\s+(.+)$", r"SECTION: \1", text, flags=re.M)
    # table rows -> plain dash-separated text rows; drop separator rows
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                continue
            lines.append("  - " + " — ".join(c for c in cells if c))
        else:
            lines.append(line)
    text = "\n".join(lines)
    # collapse the whitespace holes left behind
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def build_request(base_url: str, api_key: str, path: str, payload=None):
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    return req


def api_call(base_url: str, api_key: str, path: str, payload=None, timeout: int = 300):
    """GET/POST with retry on transient errors. Returns parsed JSON."""
    url = base_url.rstrip("/") + path
    last = None
    for attempt in range(3):
        req = build_request(base_url, api_key, path, payload)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                last = f"HTTP {e.code}: {body[:300]}"
                wait = 2 ** (attempt + 1)
                print(f"  transient HTTP {e.code}, retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"API error HTTP {e.code} from {url}:\n{body[:1000]}")
        except urllib.error.URLError as e:
            if attempt < 2:
                last = str(e)
                wait = 2 ** (attempt + 1)
                print(f"  connection problem ({e}), retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"Could not reach {url}: {e}")
    sys.exit(f"API failed after retries: {last}")


def list_models(base_url: str, api_key: str, timeout: int):
    out = api_call(base_url, api_key, "/models", timeout=timeout)
    for m in out.get("data", []):
        print(m.get("id", "?"))


def main():
    p = argparse.ArgumentParser(
        description="Rewrite a blog post as an informal spoken-word script."
    )
    p.add_argument("post", nargs="?", help="path to the post markdown file")
    p.add_argument("--model", default=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
                   help=f"model id (default: {DEFAULT_MODEL} or $LLM_MODEL)")
    p.add_argument("--out", help="output path (default: _audio/<post name>.script.md)")
    p.add_argument("--max-tokens", type=int, default=8000,
                   help="max output tokens (default 8000)")
    p.add_argument("--temperature", type=float, default=0.7,
                   help="sampling temperature (default 0.7)")
    p.add_argument("--timeout", type=int, default=300,
                   help="per-request timeout in seconds (default 300)")
    p.add_argument("--list-models", action="store_true",
                   help="list model ids from the endpoint and exit")
    p.add_argument("--dry-run", action="store_true",
                   help="print the cleaned article and prompt, skip the API call")
    a = p.parse_args()

    base = os.environ.get("LLM_BASE_URL", "").rstrip("/")
    key = os.environ.get("LLM_API_KEY", "")

    if a.list_models:
        if not base:
            sys.exit("Set LLM_BASE_URL first (the URL your /models list came from).")
        list_models(base, key, a.timeout)
        return

    if not a.post:
        p.error("post path required (or use --list-models)")

    try:
        raw = open(a.post, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"Cannot read {a.post}: {e}")

    article = strip_markdown(raw)
    words = len(article.split())
    target = int(words * 0.8)
    minutes = max(1, round(target / WPM))

    user_prompt = (
        "Rewrite the following article as a spoken-word script, following "
        "the rules exactly.\n\n"
        f"Target length: about {target} words (roughly {minutes} minutes "
        "spoken at a relaxed pace).\n\n"
        "ARTICLE:\n\n" + article
    )

    if a.dry_run:
        print("=== SYSTEM PROMPT ===\n")
        print(SYSTEM_PROMPT)
        print("=== USER PROMPT ===\n")
        print(user_prompt)
        print(f"\n=== {words} words in, target ~{target} words / ~{minutes} min ===")
        return

    if not base:
        sys.exit("Set LLM_BASE_URL (and LLM_API_KEY if required) first. "
                 "Try --dry-run to preview the prompt.")

    print(f"{a.post}: {words} words in -> target ~{target} words / ~{minutes} min",
          file=sys.stderr)
    print(f"Calling {a.model} at {base} ...", file=sys.stderr)

    out = api_call(base, key, "/chat/completions", payload={
        "model": a.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": a.temperature,
        "max_tokens": a.max_tokens,
    }, timeout=a.timeout)

    try:
        choice = out["choices"][0]
        script = choice["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        sys.exit(f"Unexpected API response shape:\n{json.dumps(out)[:1000]}")

    if choice.get("finish_reason") == "length":
        print("WARNING: output hit the token limit and may be cut off — "
              "rerun with a higher --max-tokens.", file=sys.stderr)

    out_path = a.out or os.path.join(
        "_audio", os.path.basename(a.post).replace(".md", ".script.md"))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(script + "\n")

    sw = len(script.split())
    print(f"Wrote {out_path} — {sw} words, ~{max(1, round(sw / WPM))} min spoken.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
