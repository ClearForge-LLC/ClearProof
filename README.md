# ClearProof

**Field notes from building production infrastructure with AI agents.
One failure, one rule.**

Almost nobody publishes their failure trail. Writeups describe the system that worked — which teaches
you what to build, and nothing about what to distrust. So the same handful of mistakes get
rediscovered independently, forever: embarrassing in isolation, invisible in aggregate.

This is the aggregate.

Every note here is a real incident from building a hardened infrastructure stack with AI agents as
builders and a human gate on every merge. Each one is sanitised, reproduced, and reduced to a rule
you can apply to a stack that looks nothing like ours.

## The notes

| Note | The rule |
|---|---|
| [Liveness Is Not Identity](notes/liveness-is-not-identity.md) | A port answering proves something is there. It does not prove it's the thing you deployed. |
| [A Flag Is Not a Control](notes/a-flag-is-not-a-control.md) | A flag that says an exposure exists is not a control. The thing that bounds it is — and it must be inside the hash. |
| [Make the Instrument Disagree With Itself](notes/make-the-instrument-disagree.md) | Before you trust a probe, feed it something it must reject. If it answers the same to both, it has told you nothing. |

## The pattern underneath

Roughly two-thirds of the interesting failures in our private record are **one bug wearing different
clothes: a check that reported success while measuring the wrong thing.**

A process-matching command that matched its own command line. A word boundary that made a search
structurally unable to find most of what it was looking for. A digest that turned out to be the
SHA-256 of empty input, so a before-and-after comparison "matched" while measuring nothing. A mock
that died where the real runtime survived, producing exactly the wrong conclusion. Two independent
checks that agreed with each other and were both wrong.

None of those was a bug in the thing being tested. **Every one was a bug in the instrument** — and
every one looked authoritative right up until something unrelated contradicted it.

That's the through-line, and it's why this repo is called what it is: **the difference between a claim
and a proof.**

## Why agents sharpen this

An agent writes the code *and* the check that validates it. Both come from the same understanding of
the problem, so **if that understanding has a hole, the hole is in both.** Corroboration between an
agent's work and an agent's verification of it is not independent evidence — it's the same reasoning,
twice.

Not an argument against agents. An argument for one specific question, asked by a human, about every
green result: *what would make this report success while being wrong?*

## How this repo holds itself to its own standard

The sanitisation gate ([`scripts/check_notes.py`](scripts/check_notes.py)) runs in CI on every push
and pull request. It scans the working tree **and every line ever added in git history** — because a
secret committed once and removed in the next commit is public forever.

And it **runs its own self-test first**, firing every rule against a known-bad sample built at
runtime, before its pass is believed. That's this repo obeying its own third note. A gate nobody has
watched fail is indistinguishable from a gate that cannot.

```
SELF-TEST PASS -- all 13 sanitisation rules fire on a known-bad sample,
the allowlist does not over-match, and the structure check goes red
```

## Reading further

- [`docs/northstar.md`](docs/northstar.md) — why this exists and the five invariants
- [`docs/architecture.md`](docs/architecture.md) — the note format, the gate, and where the raw material lives *(it isn't here, and it isn't copied here)*
- [`docs/roadmap.md`](docs/roadmap.md) — what's published, what's queued

## Licence and use

Take the rules. Use them, argue with them, tell us where they're wrong. If a note saves you an
afternoon, that's the entire point.

---

*Built by [ClearForge LLC](https://github.com/ClearForge-LLC). Notes are curated from a private
incident record; the record stays private, the lessons don't.*
