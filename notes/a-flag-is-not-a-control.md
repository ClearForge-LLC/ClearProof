# A Flag Is Not a Control

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

We pin our tool definitions. Every tool a model can see is hashed against a committed, reviewed
manifest, and a tool whose definition has drifted is refused registration rather than logged.

One of the hashed fields marks a tool as taking untrusted input. It was set correctly. It was inside
the hash. It was reviewed.

**It was not the control.**

What actually limited what that tool could reach was an allowlist — a dictionary in the code, a few
entries long, mapping permitted targets. Nothing hashed it. Nothing reviewed it as a security
artifact. Adding a fourth entry would have widened the tool's reach while its name, its description,
and its input schema stayed byte-identical.

**Pin drift: zero. Exposure: larger.** Every check would have stayed green.

## What made it invisible

The flag and the bound were in different places, and only one of them looked like security.

The flag *reads* as a control. It has a security-sounding name. It sits in a manifest next to other
security fields. Reviewing it feels like reviewing the boundary.

But the flag only **describes** a property. It says *this tool takes untrusted input.* The thing that
decides **how far that input can reach** was somewhere else entirely, wearing no such costume.

The uncomfortable part: we had already named this class. We had a rule about security gates deciding
on inputs the integrity system doesn't cover, and we went looking for instances of it. We found this
one anyway — because we'd been looking at the fields, and the answer was in what bounded them.

## The rule

> **A flag that says an exposure exists is not a control. The thing that bounds it is — and it must be inside the hash.**

The test is mechanical. For every field you treat as a security property, ask:

1. **What actually enforces this?** Name the mechanism, not the flag.
2. **Is that mechanism covered by your integrity check** — signed, hashed, pinned, reviewed?
3. **If someone changed it, what would go red?**

If the answer to (3) is "nothing," you have a label, not a boundary.

## The five places bounds hide

In our own audits, the bounding mechanism was outside the protected set in these forms:

- **an allowlist in code** — the case above
- **an environment variable** read at startup
- **runtime configuration** loaded from a file nobody diffs
- **a naming convention treated as logic** — *tools starting with `read_` are safe*
- **ordering or precedence** — first-match routing, where the position of a rule silently decides the outcome and no validator has an opinion about position

The last one is the one nobody audits. If your rules are evaluated first-match, **the order is
load-bearing** and almost certainly unprotected.

## Why agents make this sharper

An agent asked to "make this tool safe" will reliably produce the flag. Flags are legible, they match
the vocabulary of the request, and they demo well. The bound is an implementation detail three files
away, and nothing in the request draws attention to it.

The fix we landed was structural rather than cosmetic: the allowlist now **generates** the tool's
description, so the bound is inside the hashed unit by construction. Change the allowlist and the
hash moves. Change the hash and the tool is refused.

**Two manifest hashes moved when we fixed it — and that is how we knew the fix was real rather than
decorative.** A security fix that changes nothing measurable hasn't changed anything.

## The cheap version

If you take one thing:

**Point at the thing that stops the bad case. If it isn't covered by your integrity check, your integrity check is decorating.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with AI
agents as builders and a human gate on every merge. Published because the failures repeat, and
naming them makes them visible.*
