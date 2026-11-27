#!/usr/bin/env bash
#
# make_episode.sh — interactive pipeline: blog post -> spoken script -> MP3.
#
# Wraps _scripts/article2script.py (LLM rewrite into conversational script)
# and _scripts/script2audio.py (ElevenLabs voice-clone synthesis). Asks for
# each parameter; press Enter to accept any [default]. Env vars entered here
# last for this run only.
#
# Usage:  _scripts/make_episode.sh
#
# Env vars used (all optional if already exported):
#   LLM_BASE_URL, LLM_API_KEY, LLM_MODEL       for article2script.py
#   ELEVEN_API_KEY, ELEVEN_VOICE_ID, ELEVEN_MODEL  for script2audio.py

set -u
cd "$(dirname "$0")/.."     # run from the blog root regardless of invocation
trap 'echo; echo "Aborted."; exit 130' INT

ask() {  # ask "Prompt" "default"  ->  answer in $REPLY (Enter keeps default)
  local prompt="$1" def="${2:-}"
  if [ -n "$def" ]; then
    read -r -e -p "$prompt [$def]: " REPLY </dev/tty \
      || { echo; echo "Aborted."; exit 1; }
    REPLY="${REPLY:-$def}"
  else
    read -r -e -p "$prompt: " REPLY </dev/tty \
      || { echo; echo "Aborted."; exit 1; }
  fi
}

ask_secret() {  # hidden input for API keys
  read -r -s -p "$1: " REPLY </dev/tty || { echo; echo "Aborted."; exit 1; }
  echo >&2
}

echo "============================================================"
echo "  make_episode — post -> spoken script -> MP3 in your voice"
echo "  (Enter accepts any [default]; Ctrl-C aborts)"
echo "============================================================"
echo
echo "Environment:"
echo "  LLM_BASE_URL:    $([ -n "${LLM_BASE_URL:-}" ]    && echo set     || echo 'not set')"
echo "  LLM_API_KEY:     $([ -n "${LLM_API_KEY:-}" ]     && echo set     || echo 'not set')"
echo "  ELEVEN_API_KEY:  $([ -n "${ELEVEN_API_KEY:-}" ]  && echo set     || echo 'not set')"
echo "  ELEVEN_VOICE_ID: $([ -n "${ELEVEN_VOICE_ID:-}" ] && echo set     || echo 'not set')"
echo

# --- 1. Pick a post ---------------------------------------------

echo "--- 1. Pick a post ------------------------------------------"
posts=()
while IFS= read -r p; do posts+=("$p"); done \
  < <(ls _posts/*.md 2>/dev/null | sort -r | head -25)
if [ ${#posts[@]} -eq 0 ]; then
  echo "No .md files found in _posts/ — are you in the blog repo?"; exit 1
fi
i=1
for p in "${posts[@]}"; do printf '  %2d) %s\n' "$i" "$(basename "$p")"; i=$((i+1)); done
echo "  (or type a path to any .md file)"

ask "Post" "1"
POST="$REPLY"
if [[ "$POST" =~ ^[0-9]+$ ]] && [ "$POST" -ge 1 ] && [ "$POST" -le ${#posts[@]} ]; then
  POST="${posts[$((POST-1))]}"
fi
POST="${POST/#\~/$HOME}"
[ -f "$POST" ] || { echo "No such file: $POST"; exit 1; }

# --- 2. Spoken script -------------------------------------------

SCRIPT_OUT="_audio/$(basename "${POST%.md}").script.md"
echo
echo "--- 2. Spoken script (article2script.py) --------------------"
if [ -f "$SCRIPT_OUT" ]; then
  ask "  $(basename "$SCRIPT_OUT") exists — (r)egenerate or (u)se it" "u"
  case "$REPLY" in r|R) REGEN=1;; *) REGEN=0;; esac
else
  REGEN=1
fi

if [ "$REGEN" -eq 1 ]; then
  if [ -z "${LLM_BASE_URL:-}" ]; then
    ask "LLM_BASE_URL (your OpenAI-compatible endpoint, e.g. https://host/v1)" ""
    [ -z "$REPLY" ] && { echo "Cannot generate a script without it."; exit 1; }
    export LLM_BASE_URL="$REPLY"
  fi
  MODEL="${LLM_MODEL:-granite-5-0-230b-preview-r261008a}"
  while :; do
    ask "LLM model ('l' lists the endpoint's models)" "$MODEL"
    if [ "$REPLY" = "l" ]; then
      python3 _scripts/article2script.py --list-models || true
      continue
    fi
    MODEL="$REPLY"; break
  done
  ask "Temperature (0.0-1.0, higher = livelier rewrite)" "0.7"; TEMP="$REPLY"
  ask "Max output tokens" "8000"; MAXTOK="$REPLY"
  echo
  echo ">> python3 _scripts/article2script.py \"$POST\" \\"
  echo "     --model \"$MODEL\" --temperature \"$TEMP\" --max-tokens \"$MAXTOK\" --out \"$SCRIPT_OUT\""
  python3 _scripts/article2script.py "$POST" --model "$MODEL" \
      --temperature "$TEMP" --max-tokens "$MAXTOK" --out "$SCRIPT_OUT" \
    || { echo "Script generation failed."; exit 1; }
else
  echo "Using existing $SCRIPT_OUT"
fi

ask "Open the script in ${EDITOR:-vi} to review/edit before recording" "y"
case "${REPLY:0:1}" in y|Y) "${EDITOR:-vi}" "$SCRIPT_OUT" ;; esac
ask "Continue to audio generation" "y"
case "${REPLY:0:1}" in
  y|Y) : ;;
  *) echo "Stopped — script is at $SCRIPT_OUT"; exit 0 ;;
esac

# --- 3. Audio ----------------------------------------------------

echo
echo "--- 3. Audio (script2audio.py, ElevenLabs) ------------------"
if [ -z "${ELEVEN_API_KEY:-}" ]; then
  ask_secret "ELEVEN_API_KEY (input hidden)"
  [ -z "$REPLY" ] && { echo "Cannot continue without a key."; exit 1; }
  export ELEVEN_API_KEY="$REPLY"
fi

VOICE="${ELEVEN_VOICE_ID:-}"
while :; do
  if [ -n "$VOICE" ]; then
    ask "Voice ID ('l' lists your voices)" "$VOICE"
  else
    ask "Voice ID ('l' lists your voices — required)" ""
  fi
  if [ "$REPLY" = "l" ]; then
    python3 _scripts/script2audio.py --list-voices || true
    continue
  fi
  [ -n "$REPLY" ] && { VOICE="$REPLY"; break; }
  echo "  (a voice is required — clone one at elevenlabs.io or set ELEVEN_VOICE_ID)"
done

ask "TTS model (eleven_v3 keeps [pause] tags, v2 is the stable default)" \
   "${ELEVEN_MODEL:-eleven_multilingual_v2}"
TTSMODEL="$REPLY"

STAB=0.5; SIM=0.85; STYLE=0.2
ask "Adjust voice settings (stability / similarity / style)" "n"
case "${REPLY:0:1}" in
  y|Y)
    ask "  Stability (lower = more varied delivery)" "$STAB";   STAB="$REPLY"
    ask "  Similarity boost (how closely it sticks to your voice)" "$SIM"; SIM="$REPLY"
    ask "  Style (expressiveness — keep low for clones)" "$STYLE"; STYLE="$REPLY"
    ;;
esac

DEF_MP3="${SCRIPT_OUT%.script.md}.mp3"
ask "Output MP3 (put it under audio/ if you want it published)" "$DEF_MP3"
MP3OUT="$REPLY"

echo
echo ">> python3 _scripts/script2audio.py \"$SCRIPT_OUT\" \\"
echo "     --voice \"$VOICE\" --model \"$TTSMODEL\" \\"
echo "     --stability $STAB --similarity $SIM --style $STYLE --out \"$MP3OUT\""
python3 _scripts/script2audio.py "$SCRIPT_OUT" --voice "$VOICE" \
    --model "$TTSMODEL" --stability "$STAB" --similarity "$SIM" \
    --style "$STYLE" --out "$MP3OUT" \
  || { echo "Audio generation failed."; exit 1; }

# --- Done ---------------------------------------------------------

echo
echo "============================================================"
echo "  Done."
echo "    script : $SCRIPT_OUT"
echo "    audio  : $MP3OUT"
echo "  To publish: move the MP3 into audio/, then add a player"
echo "  to the post (I can wire an {% include audio.html %} when"
echo "  you have an MP3 you're happy with)."
echo "============================================================"
