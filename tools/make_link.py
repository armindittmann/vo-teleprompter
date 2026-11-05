#!/usr/bin/env python3
"""Build a share link for the VO teleprompter.

Usage: make_link.py <project> <textfile> [--base URL]
The text is deflate-compressed and base64url-encoded into the URL #hash,
so it is never sent to the web server.
"""
import base64, os, sys, urllib.parse, zlib

BASE = os.environ.get("TP_BASE", "http://localhost:8000/")
args = sys.argv[1:]
if "--base" in args:
    i = args.index("--base"); BASE = args[i + 1]; del args[i:i + 2]
if len(args) != 2:
    sys.exit(__doc__)
project, path = args
raw = open(path, encoding="utf-8").read().strip().encode("utf-8")
c = zlib.compressobj(9, zlib.DEFLATED, -15)
z = c.compress(raw) + c.flush()
b64 = lambda b: base64.urlsafe_b64encode(b).decode().rstrip("=")
t = "z" + b64(z) if len(z) < len(raw) else "b" + b64(raw)
print(BASE + "#p=" + urllib.parse.quote(project) + "&t=" + t)
