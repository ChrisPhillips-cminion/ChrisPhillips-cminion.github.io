---
layout: post
date: 2026-11-25 18:00:00
categories: DataPower
title: "Scripting `oc attach` into DataPower gateway pods: fixing the no-TTY 500"
author: ["ChrisPhillips", "IBMBob"]
description: "Why `oc attach -i` fails with a 500 on DataPower gateway containers, and a Python wrapper that types a command file into the console over a real pseudo-terminal — with repeat-collection support for the IBM getData.sh workflow."
tags: [DataPower, APIConnect, OpenShift, oc, Troubleshooting, Automation]
---

IBM DataPower  support asks for the usual collection when a gateway is pegged at 100% CPU: run `getData.sh`, which pipes a command file into the pod seven times, five minutes apart. On a current gateway pod that script dies immediately:

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

## Full script

```python
#!/usr/bin/env python3
"""
attach_wrapper.py — scriptable `oc attach` for TTY-only container consoles,
with built-in repeat-collection support.

Problem
-------
`oc attach -i <pod> < file` fails on containers whose console was created
with `tty: true` (e.g. IBM DataPower gateway pods):

    $ oc attach -i gwv6-0 < cli.txt
    Unable to use a TTY - input is not a terminal or the right kind of file
    Error from server:

When stdin is not a real terminal, oc silently drops the tty flag from the
attach request. The kubelet then refuses to attach a non-TTY client to a
TTY container and the API server answers 500 with an empty body — no data
ever flows.

Fix
---
This wrapper runs `oc attach -it` on a pseudo-terminal (pty) of its own, so
oc keeps tty=true (matching the container), then "types" your command file
into that pty line by line and captures everything the container prints
back to a local file.

Examples
--------
    # single collection
    python3 attach_wrapper.py --pod gwv6-0 --namespace apic-nonha \
        --container datapower --input cli.txt --output cli_output.

    # 7 collections, 5 minutes apart (like the original getData.sh)
    python3 attach_wrapper.py --pod gwv6-0 -n apic-nonha -c datapower \
        --input cli.txt --output cli_output. --iterations 7 --sleep 300

Only the Python standard library is used — works with plain `python3` or
`uv run python`.
"""

import argparse
import os
import pty
import re
import select
import subprocess
import sys
import time
from pathlib import Path

# Console states we consider "ready for the next line":
#   DataPower prompts  :  idg[apiconnect]#   /   idg(apiconnect)>
#   Login prompts      :  login:   /   Password:
PROMPT_RE = re.compile(rb"(?:login:\s*$|Password:\s*$|[#>]\s*$)")


class AttachSession:
    LOGIN_PROMPT = b"login:"

    def __init__(self, cmd, output_path, echo=True, header=None):
        self.cmd = cmd
        self.echo = echo
        # append mode: the file may already hold the iteration header
        self.out_f = open(output_path, "ab")
        if header:
            self.out_f.write(header.encode() + b"\n")
            self.out_f.flush()
        self.buf = bytearray()          # rolling tail of received output
        self.proc = None
        self.master = None
        self.login_prompts = 0          # how often the console asked to log in

    # ------------------------------------------------------------------ setup
    def start(self):
        master, slave = pty.openpty()
        self.master = master
        # oc gets the slave as stdin/stdout/stderr -> it sees a real TTY,
        # keeps tty=true in the attach request, and raw-mods the pty itself.
        self.proc = subprocess.Popen(
            self.cmd, stdin=slave, stdout=slave, stderr=slave, close_fds=True
        )
        os.close(slave)

    # ------------------------------------------------------------------ i/o
    def _write_out(self, data: bytes):
        self.buf.extend(data)
        if len(self.buf) > 65536:               # keep only the recent tail
            del self.buf[:32768]
        self.login_prompts += data.count(self.LOGIN_PROMPT)
        self.out_f.write(data)
        self.out_f.flush()
        if self.echo:
            try:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except BrokenPipeError:
                self.echo = False        # stdout gone; keep capturing to file

    def read_once(self, timeout):
        """Return pending pty output (b'' on timeout) or None on EOF/child exit."""
        if self.master is None:
            return None
        r, _, _ = select.select([self.master], [], [], timeout)
        if not r:
            return b""
        try:
            return os.read(self.master, 65536)
        except OSError:                          # EIO — pty closed
            return None

    def send_line(self, line: str):
        if self.master is None:
            return
        try:
            os.write(self.master, line.encode() + b"\n")
        except OSError as exc:
            print(f"[WARN] write to pty failed: {exc}", file=sys.stderr)

    # ------------------------------------------------------------------ states
    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def at_prompt(self):
        return PROMPT_RE.search(bytes(self.buf[-512:])) is not None

    def wait_for_prompt(self, timeout):
        """Read output until a prompt appears. True=prompt, False=timeout/EOF."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.alive():
                return False
            data = self.read_once(0.5)
            if data is None:
                return False
            if data:
                self._write_out(data)
                if self.at_prompt():
                    return True
        return False

    def drain(self, idle_timeout, overall_timeout):
        """Keep reading until the console goes quiet (or limits are hit)."""
        deadline = time.monotonic() + overall_timeout
        last_data = time.monotonic()
        while time.monotonic() < deadline:
            if not self.alive():
                break
            data = self.read_once(0.5)
            if data is None:
                break
            if data:
                self._write_out(data)
                last_data = time.monotonic()
            elif time.monotonic() - last_data > idle_timeout:
                break

    # ------------------------------------------------------------------ teardown
    def stop(self):
        """Detach: killing the local oc client never touches the container."""
        if self.alive():
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        if self.master is not None:
            try:
                os.close(self.master)
            except OSError:
                pass
            self.master = None
        self.out_f.close()


def run_capture(args, lines, outpath, iteration, total):
    """Attach once, type the file, capture output. Returns True on success."""
    cmd = ["oc", "attach", "-it", args.pod]
    if args.namespace:
        cmd += ["-n", args.namespace]
    if args.container:
        cmd += ["-c", args.container]

    print(f"[INFO] iteration {iteration}/{total}: {' '.join(cmd)}", file=sys.stderr)

    header = (f" *********** Number = {iteration} of {total} "
              f"({time.ctime()}) **************")
    sess = AttachSession(cmd, outpath,
                         header=f"Data collect started at {time.ctime()}\n{header}")
    sess.start()
    try:
        # ---- 1. connect & wait for a prompt --------------------------------
        got_prompt = sess.wait_for_prompt(args.connect_timeout)
        if not got_prompt and sess.alive() and not sess.buf:
            # Console printed its prompt before we attached; nudge it to
            # repaint (same trick oc itself suggests: "try pressing enter").
            sess.send_line("")
            got_prompt = sess.wait_for_prompt(args.connect_timeout)
        if not sess.alive():
            rc = sess.proc.returncode if sess.proc is not None else "n/a"
            print(f"[ERROR] oc attach exited early (rc={rc}); "
                  f"see {outpath}", file=sys.stderr)
            return False

        # ---- 1b. reset the console state ----------------------------------
        # A bare Enter clears a half-finished Password: prompt (it fails
        # harmlessly for whatever bogus user was pending) so that line 1
        # of the input file is always consumed as the *username*.
        sess.send_line("")
        sess.wait_for_prompt(args.line_timeout)

        # ---- 2. type the file, one line at a time --------------------------
        for i, line in enumerate(lines, 1):
            if not sess.alive():
                print(f"[ERROR] oc attach died at line {i}", file=sys.stderr)
                return False
            if sess.login_prompts >= 3:
                print("[ERROR] the console keeps asking for login — the "
                      "credentials on lines 1-2 of the input file were "
                      "rejected. Aborting to avoid an account lockout.",
                      file=sys.stderr)
                return False
            sess.send_line(line)
            sess.wait_for_prompt(args.line_timeout)

        # ---- 3. drain anything still coming back ---------------------------
        sess.drain(args.idle_timeout, args.drain_timeout)
        return True
    finally:
        sess.stop()


def main():
    ap = argparse.ArgumentParser(
        description="Feed a command file into `oc attach` (works around the "
                    "no-TTY 500 error on tty:true containers), with optional "
                    "repeat collections.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--pod", required=True, help="pod to attach to (e.g. gwv6-0)")
    ap.add_argument("-n", "--namespace", default=None, help="namespace/project")
    ap.add_argument("-c", "--container", default=None, help="container name")
    ap.add_argument("--input", required=True,
                    help="file whose lines are typed into the console")
    ap.add_argument("--output", default="cli_output.",
                    help="output filename PREFIX — each iteration writes "
                         "PREFIX<YYYYmmdd-HHMMSS>")
    ap.add_argument("--iterations", type=int, default=1,
                    help="how many collection rounds to run")
    ap.add_argument("--sleep", type=float, default=300.0,
                    help="seconds to sleep between iterations (not after the last)")
    ap.add_argument("--connect-timeout", type=float, default=30.0,
                    help="max seconds to wait for the console prompt")
    ap.add_argument("--line-timeout", type=float, default=30.0,
                    help="max seconds to wait for the prompt after each line")
    ap.add_argument("--idle-timeout", type=float, default=15.0,
                    help="stop draining after this many silent seconds")
    ap.add_argument("--drain-timeout", type=float, default=60.0,
                    help="max seconds for the final output drain")
    ap.add_argument("--fallback-exec", action="store_true",
                    help="accepted for compatibility; no longer needed — "
                         "the wrapper allocates a real TTY so attach works")
    args = ap.parse_args()

    if args.iterations < 1:
        sys.exit("[ERROR] --iterations must be >= 1")
    if args.sleep < 0:
        sys.exit("[ERROR] --sleep must be >= 0")

    inpath = Path(args.input)
    if not inpath.is_file():
        sys.exit(f"[ERROR] input file not found: {inpath}")
    lines = inpath.read_text().splitlines()
    if not lines:
        sys.exit(f"[ERROR] input file is empty: {inpath}")

    ok_all = True
    try:
        for i in range(1, args.iterations + 1):
            ts = time.strftime("%Y%m%d-%H%M%S")
            outpath = f"{args.output}{ts}"
            ok = run_capture(args, lines, outpath, i, args.iterations)
            print(f"[INFO] Created file: {outpath}", file=sys.stderr)
            ok_all = ok_all and ok
            if not ok:
                # don't keep hammering a broken state (e.g. bad credentials)
                break
            if i < args.iterations:
                print(f"[INFO] sleeping {args.sleep:g}s before next iteration",
                      file=sys.stderr)
                time.sleep(args.sleep)
    except KeyboardInterrupt:
        print("\n[INFO] interrupted — exiting", file=sys.stderr)
        sys.exit(130)

    print("[INFO] Complete", file=sys.stderr)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()


```

## Limitations and Notes

- Prompt detection is tuned to DataPower prompts. Another appliance with a different prompt means changing `PROMPT_RE` in the script.
- Output is bounded by the drain timeouts. A long `diag` burst stops being captured after 15 silent seconds or 60 seconds overall — raise `--idle-timeout` and `--drain-timeout` if you need more.
- The input file contains the admin credentials in plain text. Delete it when the collection finishes.
- Detaching kills only the local `oc` client. The container keeps running, but the console session on the appliance stays open until it times out — the same behaviour as closing a terminal window.

## Summary

`oc attach -i` cannot drive a TTY-only console, and DataPower gateway pods are TTY-only. The wrapper presents a real pseudo-terminal to `oc`, types the file at console speed, and captures the transcript — which keeps the L2 collection workflow (`getData.sh`, seven samples, five minutes apart) working unchanged.
