# The Tip That Advertised Its Scaffold

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A work-order branch was mid-repair. A large module had been wiped by accident while probing a write path. The restore was underway: first a placeholder string where the file should be, then a loading marker, then a split into smaller modules and a rebuild.

Every one of those states was **pushed to the open pull request tip**.

Nobody intended any of them as the product. They were private scaffolding for a recovery that eventually succeeded. Review later confirmed the dual-pass tip was recovered and complete. The intermediate tips were not.

While they existed, anyone — a teammate, a CI job, a merge gate, a bot reading the live tip — could observe the pull request tip as **placeholder content pretending to be the tree**. The PR page, the branch tip, and every tool that trusts "latest on the branch" were advertising a state nobody meant to publish.

The recovery worked. The lesson is not that the file was lost forever. It is that **a live tip is already a published surface**, and scaffolding on it is a ship, not a private draft.

## What made it dangerous

- **The PR stayed "open and green-looking" in the ordinary queue.** Title, description, and later review status described the intended cure. Nothing on the surface said "tip is currently a placeholder."
- **Observers had no second channel.** A bot or reviewer fetching the tip gets whatever the tip is. There is no banner that says "mid-repair; ignore me."
- **History keeps the embarrassing states forever**, even after the tip is fixed — but the acute risk is the window while the tip *is* the scaffold.
- **It pairs with a different failure we already published.** *The Artifact That Rotted in Place* is about an unchanged PR becoming a silent revert because the *base* moved. This is the twin about the *tip*: the artifact changes, and the change is a state nobody meant anyone else to treat as real.

## Why the usual instincts do not fire

We treat a branch tip as a workbench: push often, fix later. That instinct is fine for commits that still represent *attempted product*. It fails when the push is deliberately non-product — a wipe, a URI string stuffed into a source file, a `LOADING` marker — and is left as HEAD.

"It will only be there for a minute" is not a control. CI, reviewers, and other agents do not wait for your minute. A tip that exists is a tip that can be read, tested, or merged-from.

Partial restores feel like progress because each push moves *toward* the recovery. From outside, each push is a complete claim: **this is the current tree**.

## What it cost

Nothing permanent in the product — the tip was rebuilt and dual-passed. The cost was process: Review had to reconstruct a wipe → placeholder → rebuild trail from git history after the durable FEEDBACK note about it had already been overwritten by a later work order. The lesson almost vanished from the working tree for exactly the reason this note exists as a class: **findings that only live on a per-WO FEEDBACK tip evaporate when the next WO replaces the file.**

The near-miss is the finding. Had someone merged, rebased onto, or automated against the tip during the placeholder window, they would have shipped or built on content nobody intended to publish.

## The rule

> **Never leave a live pull-request tip on placeholder or loading content. Push atomic restores only.**

A tip is a published surface. Scaffolding belongs in the workbench that is not yet pushed, or in a single commit that jumps from last-good to next-good without parking the in-between as HEAD.

What we now do:

- **Restore off-tip, then push once.** Rebuild the file (or the split) locally or in a throwaway state; push only when the tip would again be intended product.
- **Treat wipe / placeholder / `LOADING` as stop conditions for HEAD.** If the only way to continue is a non-product tip, stop and change the write path — do not "probe" by publishing broken trees.
- **Prefer atomic replace over staged public scaffolding.** One commit from last-good to restored-good beats three commits that advertise the injury.
- **Promote durable lessons before the next WO overwrites `FEEDBACK.md`.** Per-WO feedback is disposable by design; ClearProof (or architecture, or Linear) is where a portable rule must land, or it vanishes with the working tree.

The signature: **the recovery succeeds, the final tip is correct, and for a stretch of time the live tip was something nobody would have agreed to publish.**
