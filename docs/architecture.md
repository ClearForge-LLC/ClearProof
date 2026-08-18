# ClearProof — Architecture

**What this is:** the shape of a note, the gate that lets one publish, and where the raw material lives.
**Invariant authority:** `northstar.md`, cited as `CP<n>`.
**Date:** 2026-08-18 · **Author:** Claude (architect) · **Gate:** Scotty.

> **This document is deliberately thin.** ClearProof is a content repo with one script. Padding it
> into something that looks like a system would be its own small dishonesty.

---

## 1. Design principles

1. **One failure, one rule, one note.** A note that teaches two things teaches neither memorably.
2. **The incident before the lesson.** Lead with what broke. The rule is earned, not announced.
3. **Name the luck.** Where a failure was caught by accident rather than by a control, say so. Most writeups quietly imply diligence.
4. **Sanitise structurally, not carefully.** Care fails on a bad night; a gate that runs on every push does not.
5. **The raw record stays private and stays put.** Notes are curated *from* it, never a second copy *of* it.

## 2. Note format

`notes/<slug>.md`, and the gate enforces the load-bearing parts:

| Section | Required | Purpose |
|---|---|---|
| `# Title` (H1) | **yes** | The rule, phrased as the thing to remember |
| `## The incident` | **yes** (CP2) | What actually broke, concretely |
| *(analysis section)* | no | Why it was invisible — usually the most valuable part |
| `## The rule` | **yes** | The portable statement, plus how to apply it |
| *(agent section)* | no | Why the class sharpens when an agent writes both the code and its check |
| `## The cheap version` | no | One sentence for a reader who skims |

Placeholders (`TODO`, `TBD`, `FIXME`) are rejected. **Notes ship finished.**

## 3. The gate

`scripts/check_notes.py`, run by `.github/workflows/gate.yml` on every push and pull request.

**Three jobs, in this order — and the order is the point:**

1. **`--self-test` first.** Every sanitisation rule is fired against a known-bad sample built at runtime, and the structure check is proven to go red. **A gate's pass is not believed until its failure has been demonstrated** (CP4).
2. **Sanitisation and structure** over `notes/` and `README.md`.
3. **Git history scan** over every line ever added to those paths. A secret committed once and removed in the next commit is public forever, so the working tree being clean proves nothing.

**Thirteen sanitisation rules** cover credential shapes (token, JWT, secret-key, PEM), owned hostnames,
tunnel and tenant hostnames, device and operator filesystem paths, IPs, UUIDs, long hex, and email.
An allowlist permits documentation placeholders (`example.com`, `127.0.0.1`, `<REDACTED>`).

**Patterns are assembled from fragments rather than written as literals** wherever a literal would
itself look like a credential — storing a token-shaped string in a public repo trips secret scanners
and is precisely the mistake the file exists to prevent.

## 4. Where the raw material lives

**It is not here, and it is not copied here.**

| Material | Home | Why |
|---|---|---|
| Numbered findings, with reproduction | `FEEDBACK.md` in each private repo | Born there, linked to the work order that produced it |
| Cross-project synthesis | the private knowledge vault | Durable, spans repos, outlives the session |
| Published notes | **here** | The only public surface |

**Provenance runs one way.** When a finding becomes a note, the *private* record is stamped with the
note's slug. Nothing here points inward, and nothing is kept in sync — a second copy of the corpus
would drift the first time one side was edited alone.

## 5. Ground truth — measured, not assumed

The gate was built and then **run against its own seed notes and its own history**, which changed two
things about it.

| Belief before | What measurement showed |
|---|---|
| A working-tree scan is sufficient | It is not. A secret committed once and reverted in the next commit is public forever, so the history scan was added as a **separate step** rather than an option |
| Sanitisation patterns can be written as literals | Writing a token-shaped literal into a public repo trips secret scanning and *is* the mistake the file prevents. Patterns are now **assembled from fragments** and the self-test builds bad samples **at runtime** |
| Self-test can run after the real check | Wrong order. If the gate is broken, the pass is meaningless — so the self-test runs **first**, and the pass is not believed until the failure has been demonstrated |
| An email pattern is simple | It over-matched documentation placeholders until the allowlist was added; over-matching trains people to ignore the gate, which is its own failure mode |

## 6. Ratified rulings

| Question | Ruling | Reason |
|---|---|---|
| Where does the raw corpus live? | **In the private repos where it was born.** No staging copy. | A second copy drifts the first time one side is edited alone — the two-sources-of-truth defect this stack has already paid for once |
| Is sanitisation a checklist or CI? | **CI, on every push and PR, blocking.** | Care fails on a bad night. A gate does not |
| Does the gate scan history? | **Yes, as its own step.** | The working tree being clean says nothing about what is recoverable from git |
| Is a private staging repo needed? | **No, until proven otherwise.** If drafts start sitting half-finished for weeks, a `drafts/` directory here — private first, flipped public later — costs almost nothing | Design for the problem you have |
| Scheduled cadence? | **No. Publish when a note earns it.** | A missed cycle feels like failure and kills the habit. The queue is already full; the work is editing, never manufacturing |

## 7. Security posture

**This repo's threat model is inverted from every other repo in the fleet.** Elsewhere the risk is
someone getting *in*. Here the risk is something getting *out* — and the raw material is private
incident reports whose interesting details are exactly the identifying ones.

- **The gate is the boundary** (CP1), enforced in CI, over the tree **and** git history.
- **The gate is proven able to fail** before its pass is believed (CP4). This is the repo's own doctrine applied to itself.
- **Action SHAs are pinned**, not floating tags — a tag is a mutable pointer and CI runs with repository access.
- **Workflow permissions are `contents: read`.** The gate never needs write.
- **No secrets are configured on this repo.** If a workflow ever needs one, that is a design change, not a settings change.

## 8. Open questions

| Question | Decider | Blocks |
|---|---|---|
| Cadence — publish on a schedule, or when a note earns it? | Scotty | Nothing; default is *when earned* |
| Whether client-derived lessons appear at all, and under what consent | Scotty + the client | Any SNA-derived note |
| Whether notes are cross-posted or only linked | Scotty | Nothing |

## 9. Amendments

| Date | Change | Rationale |
|---|---|---|
| 2026-08-18 | Created. | See `northstar.md` §7. |
