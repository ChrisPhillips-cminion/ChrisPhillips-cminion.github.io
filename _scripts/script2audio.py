#!/usr/bin/env python3
"""
script2audio.py — turn a generated spoken-word script into an MP3 in the
author's cloned voice, via the ElevenLabs API.

One-time setup (the only manual part):
  1. ElevenLabs account -> Voices -> Add Voice -> Instant Voice Clone:
     upload 1-3 minutes of clean audio of you (or more, for a Professional
     Voice Clone on a Creator+ plan), record the consent statement.
  2. Profile -> API Keys -> create a key.
  3. export ELEVEN_API_KEY=...   export ELEVEN_VOICE_ID=...   (or use --voice)

Usage:
  python3 _scripts/script2audio.py --list-voices
  python3 _scripts/script2audio.py _audio/2026-11-29-api-governance-enabling-scale.script.md
  python3 _scripts/script2audio.py script.md --model eleven_v3 --out audio/governance.mp3

Long scripts are split into chunks (ElevenLabs caps characters per request),
synthesised separately, and stitched with ffmpeg. [pause] markers written by
article2script.py are kept for eleven_v3 (which understands audio tags) and
converted to "..." for other models.

Stdlib only; ffmpeg used for stitching if present (byte-concat fallback).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.elevenlabs.io"
DEFAULT_MODEL = "eleven_multilingual_v2"
CHUNK_CHARS = 4000  # safely under per-request caps on paid tiers


# ---------- text preparation ----------

def clean_script(text: str, keep_audio_tags: bool) -> str:
    """Strip markdown remnants; conditionally keep [pause]-style audio tags."""
    text = re.sub(r"^#{1,6}\s+(.+)$", r"\1", text, flags=re.M)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)      # links
    text = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", text)          # bold/italic
    text = re.sub(r"`([^`]*)`", r"\1", text)                  # inline code
    if not keep_audio_tags:
        # only eleven_v3 understands bracketed audio tags; for everything
        # else render [pause] as an ellipsis so the voice actually pauses
        text = re.sub(r"\[\s*pause\s*\]", " ... ", text, flags=re.I)
        text = re.sub(r"\[\s*(whispers?|laughs?|sighs?|excited|sarcastic)\s*\]",
                      "", text, flags=re.I)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def split_sentences(paragraph: str):
    return [s for s in re.split(r"(?<=[.!?])\s+", paragraph) if s]


def chunk_text(text: str, limit: int):
    """Split on paragraph boundaries; hard-split oversized paragraphs by sentence."""
    chunks, cur = [], ""
    for para in (p.strip() for p in text.split("\n\n") if p.strip()):
        pieces = [para]
        if len(para) > limit:  # pathological paragraph: regroup by sentence
            pieces, run = [], ""
            for sent in split_sentences(para):
                if run and len(run) + 1 + len(sent) > limit:
                    pieces.append(run)
                    run = sent
                else:
                    run = f"{run} {sent}".strip()
            if run:
                pieces.append(run)
        for piece in pieces:
            if cur and len(cur) + 2 + len(piece) > limit:
                chunks.append(cur)
                cur = piece
            else:
                cur = f"{cur}\n\n{piece}".strip()
    if cur:
        chunks.append(cur)
    return chunks


# ---------- ElevenLabs API ----------

def get(api_key: str, path: str, timeout: int):
    req = urllib.request.Request(API_BASE + path)
    req.add_header("xi-api-key", api_key)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        sys.exit(f"ElevenLabs error HTTP {e.code} on {path}:\n{body[:600]}\n"
                 f"(401 = bad API key)")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {API_BASE}: {e}")


def synthesize(api_key: str, voice_id: str, model: str, text: str,
               settings: dict, out_path: str, timeout: int):
    """One TTS call; retries on rate limits and transient server errors."""
    url = (f"{API_BASE}/v1/text-to-speech/{voice_id}?"
           + urllib.parse.urlencode({"output_format": "mp3_44100_128"}))
    payload = {"text": text, "model_id": model, "voice_settings": settings}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", "application/json")

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                with open(out_path, "wb") as f:
                    shutil.copyfileobj(r, f)
                return
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            retry_after = e.headers.get("retry-after") if e.headers else None
            transient = e.code == 429 or e.code >= 500
            if transient and attempt < 3:
                wait = int(retry_after) if retry_after else 5 * (attempt + 1)
                print(f"  HTTP {e.code}, waiting {wait}s ...", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"ElevenLabs error HTTP {e.code}:\n{body[:600]}\n"
                     f"(401 = bad API key; 422 = check voice id / model)")
        except urllib.error.URLError as e:
            if attempt < 3:
                print(f"  connection problem ({e}), retrying ...", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"Could not reach {API_BASE}: {e}")


def list_voices(api_key: str, timeout: int):
    data = get(api_key, "/v1/voices", timeout)
    voices = data.get("voices", [])
    if not voices:
        print("No voices on this account yet — create the clone first "
              "(see header of this script).")
    for v in voices:
        print(f"{v.get('voice_id', '?'):45} {v.get('name', '?')}"
              f"  [{v.get('category', '?')}]")
    try:  # show remaining monthly characters, as a cost sanity check
        sub = get(api_key, "/v1/user/subscription", timeout).get("subscription", {})
        used, limit = sub.get("character_count"), sub.get("character_limit")
        if used is not None and limit is not None:
            print(f"\ncharacters used this month: {used} / {limit}")
    except Exception:
        pass


# ---------- stitching ----------

def stitch(chunk_files, out_path: str):
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        listfile = os.path.join(os.path.dirname(chunk_files[0]), "list.txt")
        with open(listfile, "w") as f:
            for c in chunk_files:
                f.write("file '" + os.path.abspath(c) + "'\n")
        r = subprocess.run(
            [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", listfile,
             "-c:a", "libmp3lame", "-b:a", "128k", out_path],
            capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"ffmpeg failed:\n{r.stderr[:600]}")
    else:  # fallback: plain byte concatenation (players usually cope)
        with open(out_path, "wb") as out:
            for c in chunk_files:
                with open(c, "rb") as f:
                    shutil.copyfileobj(f, out)


def duration_of(path: str):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    r = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


# ---------- main ----------

def main():
    p = argparse.ArgumentParser(
        description="Turn a spoken-word script into an MP3 via ElevenLabs.")
    p.add_argument("script", nargs="?", help="script .md from article2script.py")
    p.add_argument("--voice", default=os.environ.get("ELEVEN_VOICE_ID", ""),
                   help="voice id ($ELEVEN_VOICE_ID)")
    p.add_argument("--model", default=os.environ.get("ELEVEN_MODEL", DEFAULT_MODEL),
                   help=f"TTS model (default {DEFAULT_MODEL}; eleven_v3 keeps "
                        f"[pause] audio tags)")
    p.add_argument("--out", help="output mp3 (default _audio/<name>.mp3)")
    p.add_argument("--stability", type=float, default=0.5)
    p.add_argument("--similarity", type=float, default=0.85)
    p.add_argument("--style", type=float, default=0.2)
    p.add_argument("--chunk-chars", type=int, default=CHUNK_CHARS,
                   help=f"max characters per API call (default {CHUNK_CHARS})")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--list-voices", action="store_true")
    p.add_argument("--dry-run", action="store_true",
                   help="show chunking and character usage, no API calls")
    a = p.parse_args()

    api_key = os.environ.get("ELEVEN_API_KEY", "")

    if a.list_voices:
        if not api_key:
            sys.exit("Set ELEVEN_API_KEY first.")
        list_voices(api_key, a.timeout)
        return

    if not a.script:
        p.error("script path required (or use --list-voices)")
    try:
        raw = open(a.script, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"Cannot read {a.script}: {e}")

    keep_tags = "v3" in a.model
    text = clean_script(raw, keep_tags)
    chunks = chunk_text(text, a.chunk_chars)
    total = sum(len(c) for c in chunks)

    base = os.path.basename(a.script)
    default_out = os.path.join("_audio", re.sub(r"(\.script)?\.md$", "", base) + ".mp3")
    out_path = a.out or default_out

    print(f"{a.script}: {len(text.split())} words, {total} characters, "
          f"{len(chunks)} chunk(s), model {a.model}", file=sys.stderr)
    print(f"[pause] handling: {'kept as audio tags (v3)' if keep_tags else 'converted to ...'}",
          file=sys.stderr)

    if a.dry_run:
        for i, c in enumerate(chunks, 1):
            head = " ".join(c.split()[:10])
            print(f"  chunk {i}: {len(c)} chars | {head} ...")
        print(f"\nWould synthesise with voice "
              f"{a.voice or '$ELEVEN_VOICE_ID (not set!)'} -> {out_path}")
        print("Rough cost: that many characters off your monthly ElevenLabs "
              "allowance (free tier is 10k/month).")
        return

    if not api_key:
        sys.exit("Set ELEVEN_API_KEY (create one in ElevenLabs Profile -> API Keys).")
    if not a.voice:
        sys.exit("Set ELEVEN_VOICE_ID or pass --voice (find ids with --list-voices).")

    settings = {"stability": a.stability, "similarity_boost": a.similarity,
                "style": a.style, "use_speaker_boost": True}

    tmpdir = tempfile.mkdtemp(prefix="tts-")
    try:
        chunk_files = []
        for i, c in enumerate(chunks, 1):
            cf = os.path.join(tmpdir, f"chunk{i:03d}.mp3")
            print(f"  synthesising chunk {i}/{len(chunks)} ({len(c)} chars) ...",
                  file=sys.stderr)
            synthesize(api_key, a.voice, a.model, c, settings, cf, a.timeout)
            chunk_files.append(cf)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        stitch(chunk_files, out_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    size_mb = os.path.getsize(out_path) / 1e6
    msg = f"Wrote {out_path} ({size_mb:.1f} MB"
    secs = duration_of(out_path)
    if secs:
        msg += f", {int(secs // 60)}m{int(secs % 60):02d}s"
    print(msg + ")", file=sys.stderr)


if __name__ == "__main__":
    main()
