# The Artifact That Rotted in Place

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A small change was opened as a pull request: two rows added to an architecture table, recording a
ruling. It was correct, reviewed, and uncontroversial. It was also not urgent, so it sat open while a
failed phase was remediated around it.

Four merges later, someone went to land it.

The platform rendered the change as **removing roughly twelve hundred lines** — deleting a work-order
document, deleting an entire test file, and gutting two modules. Everything the remediation had just
added.

Nobody had touched the branch. Not one character of it had changed since review.

The base had. A pull request is a diff against a base commit, and that base was four merges stale. The
platform was faithfully describing what merging it *would now do*: restore its own snapshot of the
world and discard everything that arrived after.

## What made it dangerous

Not the conflict — a conflict is loud and safe. It was everything around it:

- **It had been reviewed and approved.** The approval was honest and remains correct for the change as written.
- **The title and description were accurate.** Nothing in the human-readable part of the artifact hinted at a revert.
- **It appeared in the ordinary list of open work**, indistinguishable from anything else awaiting a gate.
- **The additions were real.** Its stated purpose was to add two rows, and it does add two rows. The twelve hundred deletions are a side effect of when it was written, not of what it says.

Someone merging on a quick glance — trusting the review, the title, and the small stated scope — would
have reverted a phase of work while believing they were landing a two-line documentation fix.

## Why the usual instincts do not fire

Staleness is normally a *time* problem, and we all have intuitions about time: a week-old branch feels
risky, an hour-old one feels safe. Those intuitions are wrong here.

**Staleness is measured in merges, not days.** A branch opened this morning against a base that has
since absorbed a large refactor is far more dangerous than one opened last month against a quiet
file. Ours was under two days old.

And the artifact does not decay in any way the review process can see, because **review inspects the
change and the change never changed.** The thing that moved was underneath it. Every property a
reviewer checked is still true; the artifact simply now means something else in the world it is about
to land in.

## What it cost

Nothing, because it was caught while verifying whether it could still merge cleanly — and only then
because the merge state had been sitting in an ambiguous state long enough to be suspicious.

The near-miss is the finding. Had it merged, the remediation would have vanished from the main line
with a commit message describing a documentation change, and the next person to notice would have
been whoever eventually ran the tests that no longer existed.

We closed it unmerged and rewrote the same two rows against the current base. That took four minutes.
Rebasing a branch whose base predated an entire phase would have taken longer and carried the same
risk in a less obvious shape.

## The rule

> **An open change decays against a moving base. Staleness is measured in merges, not days — and the artifact never changes while it rots.**

Approval is a statement about a diff at a moment. It is not a statement about what merging will do
later.

What we now do:

- **Check the base distance before merging anything**, not the age. How many commits has the target absorbed since this branch left it?
- **Treat net deletions in an additive change as a stop condition.** A change described as adding two rows should not remove twelve hundred lines. The description and the diff disagreeing is the whole signal, and it is mechanical enough to automate.
- **Automate it**, because this is exactly the check a human skips when the change looks small and the review is already green. Ours now flags open changes whose base is far behind, and flags louder when the diff shows net deletions.
- **Prefer rewriting to rebasing when the base predates a phase.** If the change is small, re-author it against the current state. You get the same content and a diff that means what it says.
- **Re-review after a rebase, not before.** A rebase produces a different artifact. The prior approval was for a different one.

The signature: **the change is correct, the review is honest, the description is accurate, and
merging it does something nobody described.**
