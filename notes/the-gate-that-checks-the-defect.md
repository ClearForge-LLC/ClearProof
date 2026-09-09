# The Gate That Verifies Against the Defect

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A backup service enumerated every repository we owned and mirrored it. Its phase-completion gate —
the checklist a human runs before declaring the work done — had an item that read, in effect:

> Confirm the service lists every repository returned by the platform's per-owner listing endpoint.

That gate had been written months earlier and was perfectly reasonable at the time.

In between, we discovered that the per-owner listing endpoint **returns only public repositories**
under the credential the service uses. It had silently omitted every private repository we had. The
architecture was amended the same day: that endpoint was forbidden as an inventory source, and a
different one — which honours the credential's full grant — was mandated in its place.

The code was fixed. The tests were fixed. The gate was not.

Read literally, the gate now instructed a verifier to confirm the corpus matched **the exact source
that had caused the corpus to be wrong.** Run as written, it would have compared the mirror to the
broken listing, found them in perfect agreement, and passed. Green, signed off, phase closed, forty
percent of the data still missing.

A reviewer caught it in a work-order review, as a non-blocking note.

## Why nothing else could have caught it

This is the part worth sitting with. At the moment the gate was invalidated:

- **Every cross-reference still resolved.** The gate cited a real endpoint that really existed.
- **Every automated check passed.** There is no linter for "this instruction is now self-defeating."
- **The command in the gate ran successfully** and returned plausible output.
- **The numbers would have matched**, because both sides of the comparison came from the same wrong source.

Nothing was broken. Nothing was stale in the sense a tool can detect. The gate had simply become a
different claim than the one it was written to make, and it did so **without anyone editing it.**

The only thing that catches this is a person reading the gate for meaning and asking whether it still
tests what it claims to test. Ours did. We were lucky that the person reading it happened to have
read the amendment.

## The general shape

A ruling that forbids something does not only change the code. It changes the **status of every
check, gate, fixture and document that consumed the forbidden thing** — and those do not throw
errors when their premise is withdrawn.

The most dangerous of them are the ones written *against* the forbidden thing, because a check that
validates the system against the defect will report health with perfect confidence. It is not a
broken check. It is a working check pointed at a poisoned reference.

We had already learned that an instrument which cannot disagree tells you nothing. This is the same
disease with a longer incubation: **the instrument could disagree when it was written, and a ruling
elsewhere quietly took that ability away.**

## What it cost

Nothing, in the end — but only because the phase had already failed for the original defect, so the
gate was under unusual scrutiny. Had the endpoint bug been caught earlier and quietly patched, this
gate would have been re-run in the ordinary way and passed, and the incomplete backup would have been
formally certified complete. The certification would then have been cited later as evidence.

That is the real cost of this class: it does not produce an outage. It produces **a signed statement
that everything is fine**, which is far more durable than a bug.

## The rule

> **When a ruling forbids a source, every check that consumed it is now suspect — including the ones that enforce the ruling.**

Amending the code is the easy half. The amendment is not complete until you have found every place
that *referenced* the forbidden thing and asked, one at a time, whether it still means what it says.

Practically:

- **Make propagation part of the ruling, not follow-up work.** The change is not "fix the code"; it is "fix the code and everything that pointed at the old behaviour." Ship them together or the second half becomes optional.
- **Search for the forbidden thing by name across gates, fixtures, runbooks and acceptance criteria** — not only across source. Ours survived in a checklist, which no build tool reads.
- **A gate is not exempt from the ruling it enforces.** It is the most likely place for the old premise to survive, because gates are written once and read rarely.
- **Ask of every check: could this pass while the thing it protects against is happening?** If the answer is yes, it is not a check.

The failure has a signature worth memorising: **a check whose pass condition is satisfied by the very
defect it exists to detect.**
