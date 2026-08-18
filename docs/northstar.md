# ClearProof — Northstar

**What this is:** why this repo exists and what must stay true.
**Date:** 2026-08-18 · **Author:** Claude (architect) · **Gate:** Scotty.
**Read next:** `architecture.md` (the note format and the gate), `roadmap.md` (order).

---

## 1. The one sentence

> **ClearProof publishes the failures — named, reproduced, and stripped of anything identifying — so that the class becomes visible to someone who has not yet hit it.**

Not tutorials. Not architecture showcases. **Failures, with the rule they produced.**

## 2. The problem

Almost nobody publishes their failure trail. Writeups describe the system that worked, which teaches
the reader what to build and nothing about what to distrust. The result is a field where the same
handful of mistakes are rediscovered independently, forever, because each one is embarrassing in
isolation and invisible in aggregate.

We have the aggregate. Building a hardened infrastructure stack with AI agents as builders produced
a numbered, dated, reproduction-carrying record of every failure, because the review discipline
required one. **Roughly two-thirds of the interesting ones are the same bug in different clothes: a
check that reported success while measuring the wrong thing.**

That's a contribution, and it costs almost nothing to make — the corpus is generated whether or not
anyone publishes it.

## 3. End state

A small set of short notes, each one failure and one rule, each readable in ten minutes and
applicable the same day. A reader who has never seen this stack should be able to take the rule and
apply it to theirs.

## 4. Invariants

**Cited as `CP1`…`CP5`.** Each is falsifiable, and the gate in `scripts/check_notes.py` enforces the
first two mechanically.

| CP | Invariant | How to falsify |
|---|---|---|
| **1** | **No note leaks infrastructure.** No credential, hostname, IP, UUID, tenant, or operator path — in the working tree **or anywhere reachable in git history**. | Find one, in any commit |
| **2** | **Every note carries a reproduction.** A rule without the incident that produced it is an opinion. | Find a note with no `## The incident` |
| **3** | **Every note names what it cost us**, including where the author was wrong. Sanitised, not sanitised-of-fault. | Find a note that reads as though nobody made a mistake |
| **4** | **The gate can go red.** Its self-test proves every rule fires on a known-bad sample. | Break a rule deliberately and watch CI pass |
| **5** | **Notes are drawn from real incidents in the private record**, never invented to make a point. | Find a note with no traceable source finding |

**CP4 is here because of CP1.** A sanitisation gate nobody has watched fail is exactly the shape this
repo exists to warn about.

## 5. Non-goals

- **A framework.** No library ships from here. The output is prose and a rule.
- **Comprehensiveness.** A note publishes when it earns it. A thin catalogue of good notes beats a full one of filler.
- **Being right about everything.** Notes carry our reasoning; some of it will age badly. Amend in place with the date, don't quietly delete.
- **Client material without consent.** Work done for someone else is theirs. Generalised lessons only, and only with their agreement.

## 6. What would make this a failure

- **A leak.** One credential in one commit and the repo's whole premise is inverted. This is why CP1 is enforced against history, not just the tree.
- **It becomes a highlight reel** — failures selected for how well they flatter the eventual fix.
- **Nobody publishes.** The corpus keeps growing privately and the editing pass never happens. **This is the most likely failure and it is a scheduling failure, not a technical one.**
- **The notes get long.** The value is that a rule fits in a sentence. A 4,000-word essay is a different product with a much lower hit rate.

## 7. Amendments

| Date | Change | Rationale |
|---|---|---|
| 2026-08-18 | Created; seeded with three notes. | The private record had reached ~170 numbered findings across several repos, with a recurring class already named. Curation, not capture, was the bottleneck. |

## 8. Provenance

Written by Claude (architect) on 2026-08-18. Source material: `FEEDBACK.md` and roadmap amendments
across the private ClearForge repos. Notes are curated from that record; the record stays private.
