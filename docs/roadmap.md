# ClearProof — Roadmap

**What this is:** the order this runs in, and how each phase is known to be done.
**Date:** 2026-08-18 · **Author:** Claude (architect) · **Gate:** Scotty.
**Read first:** `northstar.md` (invariants, cited `CP<n>`), `architecture.md` (note format and gate).

## How this document works

- **Phases are dependency-ordered. No dates** — this is edited in whatever hours exist, so completion is measured by gate, not by calendar.
- **"What next" is answered here**: the first phase whose dependencies are green and whose gate has not passed.
- Invariants live in `northstar.md`, not here.

**PREFIX: `CP`.** Ids are `CP-WO-PSNN`. First id: **`CP-WO-0000`**.

> **An honest note on shape.** This is a content repo, so "phases" are lighter than in a build repo
> and the later ones are closer to habits than milestones. Saying so is better than dressing a
> publishing rhythm up as engineering.

---

## Critical path

```
  P0 gate ──► P1 seed ──► P2 backfill ──► P3 cadence
   (done)      (done)      (the work)      (the habit)
```

**Where risk concentrates: P0.** A leak is the one unrecoverable failure here, and it is
unrecoverable in the specific sense that git history is public forever. Everything after P0 is
editorial and reversible.

**The most likely failure is P3**, and it is not technical: the corpus keeps growing privately and
the editing pass never happens.

---

## P0 · The gate *(GATE PASSED — 2026-08-18)*
**Goal:** nothing can publish that leaks infrastructure, and the gate is proven able to refuse.
**Depends on:** nothing. **Invariants:** CP1, CP4.
**Exit gate:** thirteen sanitisation rules, each **fired against a known-bad sample** by
`--self-test`; the structure check demonstrated going red; the history scan running as its own step;
CI blocking on push and pull request; action SHAs pinned.

## P1 · Seed *(GATE PASSED — 2026-08-18)*
**Goal:** three notes, each a real incident with a portable rule.
**Depends on:** P0. **Invariants:** CP2, CP3, CP5.
**Exit gate:** three notes pass the gate; each names what the failure cost, **including where the
author was wrong**; each traces to a numbered finding in the private record.

## P2 · Backfill
**Goal:** mine the existing private record — several repos, ~170 numbered findings — for everything
that already earns a note.
**Depends on:** P1. **Invariants:** CP1, CP3, CP5.
**Work orders:** `CP-WO-0200`+, one per source repo.
**Known candidates:** *fix the gate, not the work* (an acceptance criterion that became uncheckable
the moment the fix worked) · *a content sweep sees writers that have written; a start-path sweep sees
writers that can* · *a wrong number that looks right is worse than a missing one* · the
architect/builder division of labour and what it actually buys.
**Exit gate:** every source repo read through once with a candidate list recorded; each candidate
either published, rejected with a reason, or **deferred pending consent** where it derives from
client work.
**Human-track:** client-derived material needs the client's agreement **before** drafting, not before
publishing.

## P3 · Cadence
**Goal:** publishing becomes a habit rather than a project.
**Depends on:** P2 producing a queue.
**Exit gate:** four notes published in four consecutive weeks **without a new work order being
written for any of them** — i.e. the editing pass has become routine.
**Deliberately not a schedule.** A missed cycle should be information, not failure. The rule is
*publish when a note earns it*; the queue exists so that is nearly always.

---

## Standing cadence

- One note per branch; one PR per note; **the gate is never bypassed, including for a one-word fix.**
- A note is drafted **from** a finding, never invented to make a point (CP5).
- **At every phase boundary:** is the README still true, has a note aged badly, did a rule get superseded by a later finding.

## Amendments

| Date | Change | Rationale |
|---|---|---|
| 2026-08-18 | Created. P0 and P1 passed on creation. | The gate and three seed notes were built in one sitting; recording them as passed phases rather than pretending they were sequenced separately. |

## Provenance

Written by Claude (architect) on 2026-08-18.
