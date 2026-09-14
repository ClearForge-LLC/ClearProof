# The Failure That Heals Its Own Symptom

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A mirroring service keeps two things per repository: a bare copy that it fetches into, and a working
checkout built from that copy. A scheduled pass asks the upstream what changed, fetches the ones that
moved, rebuilds their checkouts, and records the new state.

Failures are handled per repository. If a checkout rebuild fails, the pass logs it, increments a
consecutive-failure counter, marks the repository degraded after a few, and moves on. No state row is
written for a repository whose checkout did not build — which is correct, and was in fact a rule we
had adopted deliberately: never record a change before the thing it describes exists on disk.

That is all sound. Here is what it misses.

The fetch happens **before** the checkout rebuild. So when the fetch succeeds and the rebuild fails,
the bare copy has already advanced. The recorded state has not.

Now look at the *next* pass. It decides which repositories moved by comparing the upstream refs
against **the local bare copy**. The bare copy already fetched. They match. The repository is
classified as unchanged.

And the unchanged path — the fast, boring, nothing-to-do-here path — resets the consecutive-failure
counter to zero and clears the degraded flag.

So the update is lost permanently: the recorded state keeps the old value, the change is never
published to consumers, the checkout is never rebuilt. **And the system switches off its own alarm on
the following pass and reports healthy from then on.**

## Why this is a different animal

We have a whole shelf of notes about checks that measure the wrong thing. This is not that. Every
check here is correct in isolation:

- The failure *was* detected.
- The counter *was* incremented.
- The degraded flag *was* raised.
- The change row *was* correctly withheld.

The defect is that the recovery path cannot distinguish **"nothing needed doing"** from **"the thing
that needed doing already half-happened."** Both look identical from where it stands, because the
evidence it consults — the local copy — was advanced by the very operation that then failed.

So the system does not merely fail to notice. It **actively repairs the appearance of health** while
the underlying loss persists, and it does so through the path that exists for the common, healthy
case. The louder the healthy traffic, the faster the alarm gets cleared.

## The half-completed operation

Underneath is a mundane fact with an unpleasant consequence: an operation with two steps and no
transaction can stop in the middle, and the middle can be **indistinguishable from the end.**

Step one leaves a durable artifact. Step two fails. Later, something asks "is there work to do?" and
answers by looking at the artifact from step one. Answer: no.

This is why "record the change only after the thing exists" — a rule we adopted for good reasons and
still believe — is not sufficient on its own. It correctly prevents publishing a lie. It does nothing
about the fetch that already landed, which is now silently doing the job of a completion marker.

## What it cost

Nothing yet, and this is the only reason the note is being written now rather than after an incident:
the scheduled pass does not exist yet. The code that would run it unattended has not been built.
A reviewer found this reading the failure path during a routine adversarial pass, rated it moderate,
and proposed two cures. The severity was raised on the strength of the self-clearing alarm, which the
original rating had not accounted for, and the fix was made a hard prerequisite of ever putting the
pass on a timer.

Had it shipped scheduled, the observable symptom would have been: a repository quietly stops updating,
forever, with every dashboard green.

## The rule

> **A recovery path must not be able to clear an alarm it cannot verify. If an operation can stop half-done, the half-done state needs a name of its own.**

Two things have to be true, and fixing only the first is the trap:

1. **The half-completed state must be representable.** Either undo step one when step two fails, or record that step one landed and step two is pending. "Nothing to do" and "partially done" must not be the same observation.
2. **Clearing a failure signal requires positive evidence that the failure is gone** — not the absence of a new failure. Ours cleared on "no work detected," which is precisely the reading a half-done state produces.

Generally:

- **Never let one step's durable side effect double as the completion marker for a later step.** If it is used to decide whether work remains, it is a completion marker, whatever you meant it to be.
- **Audit every place a health signal is cleared**, and ask what evidence justified clearing it. Alarms raised on evidence and cleared on silence will always end up clear.
- **When comparing "what should be" against "what is," check that the source of "what is" was not moved by the failed operation.** Ours compared upstream against a local copy that the incomplete run had already advanced.
- **A moderate-severity finding that switches off its own detection is not moderate.** Rate the amplifier, not just the loss.
