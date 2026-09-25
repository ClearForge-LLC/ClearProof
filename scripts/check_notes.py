#!/usr/bin/env python3
"""ClearProof gate. Runs on every push and pull request.

Two jobs, and the second is the one that matters:

  1. SANITISATION — refuse anything that leaks infrastructure. This repo is public and its raw
     material is private incident reports, so the failure mode is structural rather than careless:
     the interesting details ARE the identifying ones.

  2. STRUCTURE — refuse a note that has skipped the part that makes it worth reading. A rule with
     no reproduction is an opinion.

Exits non-zero on any violation. `--self-test` proves the checker can go red, because a gate that
has only ever been seen passing is indistinguishable from a gate that cannot fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"

# --------------------------------------------------------------------------------------------
# Sanitisation. Each entry: (name, compiled pattern, why it matters).
#
# Patterns are built from fragments rather than written as literals wherever a literal would look
# like a real credential -- storing a token-shaped string in a public repo trips secret scanners
# and is exactly the mistake this file exists to prevent.
# --------------------------------------------------------------------------------------------
_GH = "gh" + "[pousr]_"
_JWT = "ey" + "J[A-Za-z0-9_-]{10,}"

RULES: list[tuple[str, re.Pattern[str], str]] = [
    ("github-token", re.compile(_GH + r"[A-Za-z0-9_]{20,}"), "GitHub token shape"),
    ("jwt", re.compile(_JWT + r"\.[A-Za-z0-9_-]{10,}"), "JWT shape"),
    ("sk-key", re.compile(r"\bsk_(?:test|live)_[A-Za-z0-9]{16,}"), "secret key shape"),
    ("pem", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    ("owned-domain", re.compile(r"\b[\w-]+\.(?:clearforge\.dev|clearuniverse\.net)\b"),
     "internal hostname"),
    ("tunnel-host", re.compile(r"\b[0-9a-f-]{8,}\.cfargotunnel\.com\b"), "tunnel hostname"),
    ("authkit-tenant", re.compile(r"\b[\w-]+\.authkit\.app\b"), "identity tenant hostname"),
    ("termux-path", re.compile(r"/data/data/com\.termux\b"), "device filesystem path"),
    ("home-path", re.compile(r"/home/[a-z][a-z0-9_]{2,}\b"), "operator home path"),
    ("public-ip", re.compile(r"\b(?!127\.0\.0\.1|0\.0\.0\.0|1\.1\.1\.1)"
                            r"(?:\d{1,3}\.){3}\d{1,3}\b"), "IP address"),
    ("uuid", re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                        r"[0-9a-f]{4}-[0-9a-f]{12}\b"), "UUID (tunnel/account/client id)"),
    ("long-hex", re.compile(r"\b[0-9a-f]{40,}\b"), "long hex (key, hash, or secret)"),
    ("email", re.compile(r"\b[\w.+-]+@(?!example\.(?:com|net|org|invalid))"
                         r"[\w-]+\.[a-z]{2,}\b"), "email address"),
]

# Placeholders a note is ALLOWED to contain. Anything meant to look like a real value must be
# obviously fake and must live here.
ALLOWED = re.compile(
    r"example\.(?:com|net|org|invalid)|127\.0\.0\.1|localhost|"
    r"<REDACTED>|your-service|myservice|REPLACE_ME",
    re.I,
)

REQUIRED_HEADINGS = ("## The incident", "## The rule")


def scan_text(text: str, label: str) -> list[str]:
    out: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        # Blank out permitted placeholders instead of skipping the line: a line that mentions
        # example.com must still be scanned for the real hostname beside it. (Found by the
        # clearseal-reference leak gate while porting these rules.)
        line = ALLOWED.sub(" ", line)
        for name, pat, why in RULES:
            m = pat.search(line)
            if m:
                out.append(f"{label}:{lineno}  [{name}] {why} -- matched {len(m.group(0))} chars")
    return out


def check_structure(path: Path, text: str) -> list[str]:
    out: list[str] = []
    if not text.lstrip().startswith("# "):
        out.append(f"{path.name}:1  [structure] no H1 title")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            out.append(f"{path.name}  [structure] missing required section '{heading}' -- "
                       f"a rule with no reproduction is an opinion")
    if re.search(r"\bTODO\b|\bTBD\b|\bFIXME\b|\[ASSUMPTION", text):
        out.append(f"{path.name}  [structure] unresolved placeholder; notes ship finished")
    return out


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    if not NOTES.is_dir():
        print("no notes/ directory", file=sys.stderr)
        return 1

    findings: list[str] = []
    files = sorted(NOTES.glob("*.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        findings += scan_text(text, path.name)
        findings += check_structure(path, text)

    for extra in ("README.md",):
        p = ROOT / extra
        if p.exists():
            findings += scan_text(p.read_text(encoding="utf-8"), extra)

    if findings:
        print(f"REFUSED -- {len(findings)} violation(s) across {len(files)} note(s):\n",
              file=sys.stderr)
        for f in findings:
            print("  " + f, file=sys.stderr)
        print("\nNothing publishes until these are clear.", file=sys.stderr)
        return 1

    print(f"OK -- {len(files)} note(s) clean against {len(RULES)} sanitisation rules "
          f"and {len(REQUIRED_HEADINGS)} structure rules")
    return 0


def self_test() -> int:
    """Prove every rule can fire. A gate only ever seen passing may be a gate that cannot fail."""
    samples = {
        "github-token": "token is " + "gh" + "p_" + "A" * 30,
        "jwt": "bearer " + "ey" + "JhbGciOiJIUzI1NiJ9" + "." + "abcdefghijklmnop",
        "sk-key": "key " + "sk_" + "test_" + "B" * 24,
        "pem": "-----BEGIN RSA PRIVATE KEY-----",
        "owned-domain": "reached api.clearforge.dev today",
        "tunnel-host": "cname to abc12345-def6.cfargotunnel.com",
        "authkit-tenant": "issuer https://some-tenant-staging.authkit.app",
        "termux-path": "lives at /data/data/com.termux/files/home",
        "home-path": "cd /home/someuser/project",
        "public-ip": "resolved to 203.0.113.9",
        "uuid": "id 88c0a74a-b520-479c-9bfb-1b8067c39f7a",
        "long-hex": "sha " + "c" * 44,
        "email": "wrote to person@realdomain.dev",
    }
    failed = []
    for name, sample in samples.items():
        hits = [h for h in scan_text(sample, "selftest") if f"[{name}]" in h]
        if not hits:
            failed.append(f"rule '{name}' did NOT fire on its own sample")

    if scan_text("see example.com and 127.0.0.1 and <REDACTED>", "selftest"):
        failed.append("allowlist leaked: a permitted placeholder was flagged")
    if not scan_text("see example.com beside abc.clearforge.dev on one line", "selftest"):
        failed.append("placeholder masked the line: a real hostname next to example.com was not flagged")

    missing = check_structure(Path("x.md"), "# Title\n\nno sections here\n")
    if len(missing) < 2:
        failed.append("structure check did not catch a note missing its required sections")

    if failed:
        print("SELF-TEST FAILED -- the gate cannot be trusted:", file=sys.stderr)
        for f in failed:
            print("  " + f, file=sys.stderr)
        return 1

    print(f"SELF-TEST PASS -- all {len(samples)} sanitisation rules fire on a known-bad sample, "
          f"the allowlist does not over-match, and the structure check goes red")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
