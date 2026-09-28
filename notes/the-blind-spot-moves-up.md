# Extraction Moves the Blind Spot

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A user-facing control was untestable. Every assertion covering it read the page's
**source text** — that the right function was called with the right arguments — because
the test runner had no way to construct the page and ask it questions. We proved how
little that was worth by mutating the code: **ten mutations deleted or inverted the
control outright, and the entire suite stayed green.** One of them simply never added
the feature to the page at all.

So we added a DOM library and rebuilt those assertions as behavioural ones. **It
worked.** All ten mutations now fail. That is a real measurement and it is still true.

Then we mutated the new work, to see what the new tests could not see.

**Forty-five mutations. Twenty-one came back green.**

Nineteen were genuine gaps; two were bad mutations that modelled nothing. But the
number was not the finding. **The finding was their distribution: they were not
scattered. They formed one contiguous band — everything exactly one layer above the
newly-testable unit.**

The harness observed the extracted function perfectly. It observed nothing that
*called* it.

## What made it invisible

The fix was genuine, measurable and correctly reported. Ten reds where there had been
ten greens is exactly the evidence you would ask for.

But two claims hide inside it and only one was earned:

* **"This defect is now caught."** True.
* **"This class of defect is now caught."** Not true, and nothing in the measurement
  distinguishes them.

Extraction creates a seam. Tests attach to the seam, because that is what made them
possible. **The code that decides whether to call across the seam is now on the far
side of it, and nothing attaches there.** The untested region did not shrink. It moved
up one storey and changed its name.

Worse, the move is self-concealing: the coverage metric improves, the mutation score
improves for the unit under test, and the reviewer sees a real before-and-after. The
band only becomes visible if you mutate the layer you did not just make testable — and
the reason to do that is precisely the reason you would not think to.

**Where we were wrong:** we treated "now testable" as "now tested," and we had
measured the first thing carefully enough that nobody asked about the second.

## The rule

> **When you extract code to make it testable, the untested region moves up to the
> caller. Mutate the caller, or you have relocated the gap and called it closed.**

How to apply it:

- **Read the distribution, not the count.** Twenty-one survivors out of forty-five is
  a coverage number, and coverage numbers invite a shrug. Twenty-one survivors *in one
  contiguous band* is a structural fact that points straight at the seam. **Always ask
  where the survivors sit relative to each other.**
- **Name the layer your new tests attach to, then mutate the one above it.** If that
  layer cannot be driven at all, the extraction is not finished — say so rather than
  reporting the improvement you did achieve.
- **Pin shape, not identifiers.** A guard in that band broke on a legitimate rename
  because it asserted a call by name. Re-pinned to the *shape* of the call, it survived
  the rename and still caught the regression. A guard that breaks on refactors teaches
  the next person to loosen it.
- **Expect the band to reappear.** Every extraction creates a new one further up. The
  question is never whether it exists; it is whether you looked.

## Why agents sharpen this

An agent asked to make something testable will extract it, test the extraction, and
report honestly that coverage improved — because it did. The instruction was satisfied.
The metric moved. **The reasoning that chose what to extract also chose what to test,
so the seam and the test boundary are the same line by construction**, and nothing in
the task prompts anyone to look just beyond it.

The correction is one sentence in the work order and it is worth the words: *mutate the
caller, not the unit, and report both numbers.*

## The cheap version

**Ask which layer your new tests attach to, then attack the layer above it. That is
where the gap went.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack
with AI agents as builders and a human gate on every merge. Published because the
failures repeat, and naming them makes them visible.*
