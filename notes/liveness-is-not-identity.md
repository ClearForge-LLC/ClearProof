# Liveness Is Not Identity

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

We deployed a new build of a service. The deploy script reported success. The service restarted cleanly. Its health endpoint returned `200`.

It was serving the previous build.

Not a partial rollout. Not a caching layer. The old code was running, answering requests, and reporting itself healthy — for as long as it took someone to notice, which was longer than it should have been.

## What actually happened

The restart step did this:

```bash
kill $(pgrep -f myservice | head -1)
```

Two processes matched. `head -1` killed one. **The survivor kept the listening socket.** The new process couldn't bind the port, exited, and the deploy script — which checked that the service was *up*, not that it was *new* — called it a success.

Then the health check confirmed it. `GET /health` → `200 OK`. Because the old build was genuinely healthy. It was just old.

## The part worth sitting with

Two independent checks agreed. **They were both wrong, in the same direction, for the same underlying reason.**

That's the bit that should make you uncomfortable. We tend to treat corroboration as evidence — if the deploy script *and* the health check both say fine, it's probably fine. But independence isn't about who's asking. It's about **what they're measuring.**

Both of ours measured *liveness*: is something there? Neither measured *identity*: is it the thing I deployed?

Agreement between two checks that share a blind spot is worth exactly nothing. It is, if anything, worse than a single check — because it manufactures confidence.

What caught it was an unrelated field in a metadata document that happened to be derived from the new configuration. Nothing designed to catch it. **Luck, wearing the costume of a control.**

## The rule

> **Liveness is not identity. A port answering proves something is there. It does not prove it's the thing you deployed.**

Concretely, after any deploy, assert something that **could only be true of the new build**:

- a version string, commit SHA, or build ID the process reports about itself
- a value derived from configuration that changed in this release
- process start time, checked against when you started the deploy
- the PID, compared against the one you killed

Any of these is cheap. None of them is `200 OK`.

And the corollary, which is the actually useful half:

> **When two checks agree, ask what they'd both miss.**

If you can't name a failure one would catch and the other wouldn't, you don't have two checks. You have one check, run twice, and a false sense of coverage.

## Why this shows up more with agents, not less

An agent building on your behalf writes the deploy script *and* the check that validates it. Both come out of the same understanding of the problem — so if that understanding has a hole, **the hole is in both.** Corroboration between an agent's work and an agent's verification of that work is not independent evidence. It's the same reasoning, twice.

That's not an argument against agents. It's an argument for the reviewer asking a specific question: *what would make this report green while being wrong?* Ask it about the code, and then ask it again about the test.

## The cheap version

If you take one thing:

**After a deploy, print something that changed. Compare it to what you expected. `200 OK` is not that thing.**

---

*This is one of a series of notes on failures we hit while building a hardened infrastructure stack with AI agents as builders and a human gate on every merge. They're published because the failures repeat, and naming them makes them visible.*
