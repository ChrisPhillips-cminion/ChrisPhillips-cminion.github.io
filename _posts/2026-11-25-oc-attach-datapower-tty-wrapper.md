---
layout: post
date: 2026-11-25 18:00:00
categories: DataPower
title: "Scripting `oc attach` into DataPower gateway pods: fixing the no-TTY 500"
author: ["ChrisPhillips", "IBMBob"]
description: "Why `oc attach -i` fails with a 500 on DataPower gateway containers, and a Python wrapper that types a command file into the console over a real pseudo-terminal — with repeat-collection support for the IBM getData.sh workflow."
tags: [DataPower, APIConnect, OpenShift, oc, Troubleshooting, Automation]
---

IBM DataPower L2 support asks for the usual collection when a gateway is pegged at 100% CPU: run `getData.sh`, which pipes a command file into the pod seven times, five minutes apart. On a current gateway pod that script dies immediately:

```
$ oc attach -i gwv6-0 -n apic-nonha -c datapower < cli.txt
Unable to use a TTY - input is not a terminal or the right kind of file
Error from server:
```

An empty error message from the server and nothing collected.

<!--more-->

## Why it fails

DataPower gateway containers are created with `tty: true`. When stdin is not a real terminal — a redirected file, a pipe — `oc` silently drops the tty flag from the attach request. The kubelet then refuses to attach a non-TTY client to a TTY container, and the API server answers 500 with an empty body. No data ever flows.

`-i` on its own will never work here. The container wants a TTY, so the client has to present one.

## The wrapper

Bob and I wrote a small Python wrapper, `attach_wrapper.py`. It runs `oc attach -it` on a pseudo-terminal of its own, so `oc` keeps `tty=true` to match the container. It then types your command file into that pty line by line and captures everything the console prints back to a local file.

Only the Python standard library is used — plain `python3` or `uv run python`, nothing to install.

### How it works

1. Allocates a pty and gives the slave end to `oc` as stdin/stdout/stderr, so `oc` sees a real terminal.
2. Waits for a prompt. Prompt detection is a regex over the tail of the received output, covering the DataPower prompts (`idg[apiconnect]#`, `idg(apiconnect)>`) plus `login:` and `Password:`.
3. If the console stays quiet, it sends a bare Enter to make it repaint — the same trick `oc` itself suggests with "If you don't see a command prompt, try pressing enter."
4. Sends another bare Enter before the first real line. This clears a half-finished `Password:` prompt (it fails harmlessly for whatever bogus user was pending), so line 1 of the input file is always consumed as the username.
5. Types each line and waits for the prompt after each one.
6. Aborts after three `login:` prompts. If the credentials on lines 1–2 of the input file were rejected, you stop rather than lock the admin account.
7. Drains anything still coming back until the console goes quiet, then detaches. Killing the local `oc` client never touches the container.

## Usage

Single collection:

```bash
python3 attach_wrapper.py --pod gwv6-0 --namespace apic-nonha \
    --container datapower --input cli.txt --output cli_output.
```

Seven collections, five minutes apart — the original getData.sh pattern:

```bash
python3 attach_wrapper.py --pod gwv6-0 -n apic-nonha -c datapower \
    --input cli.txt --output cli_output. --iterations 7 --sleep 300
```

`--output` is a filename prefix. Each iteration writes `cli_output.<YYYYmmdd-HHMMSS>` with a header recording when it started and which round it was:

```
Data collect started at Wed Nov 25 17:58:47 2026
 *********** Number = 1 of 10 (Wed Nov 25 17:58:47 2026) **************
```

The timeouts (`--connect-timeout`, `--line-timeout`, `--idle-timeout`, `--drain-timeout`) all have sane defaults. The only ones you are likely to touch are `--iterations` and `--sleep`.

## The input file

The input file is the same `cli.txt` the support script always generated: username and password on the first two lines, then the collection commands. First two lines here for illustration — do not commit this file anywhere:

```
admin
<password>
echo show clock
show clock
echo "*********BASE STATISTICS*********"
echo show load
show load
echo show cpu
show cpu
...
exit
```

Rather than hardcoding the password, pull it from the gateway's admin secret when you build the file:

```bash
oc get secret admin-secret -n apic-nonha -o jsonpath='{.data.password}' | base64 -d
```

`getData.sh` still works as the front door — it now generates `cli.txt` the same way and calls the wrapper with `--iterations` and `--sleep`. The support workflow does not change; you still send the `cli_output.*` files to IBM at the end.

What lands in the file is exactly what the console printed, prompts included:

```
idg# show load

 Task ID Task name        Load Work list CPU Memory File count
 ------- ---------------- ---- --------- --- ------ ----------
 1       main             4    1         2   12     166
 3       QuotaEnforcement 1    0         0   0      19
 ...
```

## Limitations and Notes

- Prompt detection is tuned to DataPower prompts. Another appliance with a different prompt means changing `PROMPT_RE` in the script.
- Output is bounded by the drain timeouts. A long `diag` burst stops being captured after 15 silent seconds or 60 seconds overall — raise `--idle-timeout` and `--drain-timeout` if you need more.
- The input file contains the admin credentials in plain text. Delete it when the collection finishes.
- `--fallback-exec` is accepted but does nothing — it is kept so old command lines do not break. The wrapper allocates a real TTY, so an `exec` fallback is no longer needed.
- Detaching kills only the local `oc` client. The container keeps running, but the console session on the appliance stays open until it times out — the same behaviour as closing a terminal window.

## Summary

`oc attach -i` cannot drive a TTY-only console, and DataPower gateway pods are TTY-only. The wrapper presents a real pseudo-terminal to `oc`, types the file at console speed, and captures the transcript — which keeps the L2 collection workflow (`getData.sh`, seven samples, five minutes apart) working unchanged.
