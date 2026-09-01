# Absence Needs Its Own Clock

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

We ran two AI coding sessions in a loop — one authoring work orders, one building against them, a
human gating every merge. The builder occasionally stopped partway through a task: work half done,
nothing committed, no handoff sent. Silent. The other session sat waiting for a message that was
never coming, and the human found out hours later by looking.

So we built a detector. The builder session already fired a hook whenever it finished a turn, and
that hook sent a notification. We taught it to classify: clean tree, work pushed, handoff written →
**parked**, quiet notification. Anything else → **stalled**, loud alarm.

We tested it. It correctly identified a stalled state. We shipped it.

Within minutes it was firing the loud alarm every few minutes — on a session that was working
perfectly. Ordinary mid-task turn boundaries look exactly like an abandoned one at the instant they
happen. The difference is not *state*. The difference is *whether anything happens next*.

We fixed the classifier. And in fixing it we noticed the thing that mattered:

**The hook fires when a turn ends. A stalled session ends no more turns. Our stall detector was
wired to an event that a stall makes stop happening.**

It could produce false alarms forever and true ones never. Not "unreliable" — **structurally
incapable**. The one case it existed for was precisely the case in which it was silent.

## Why this is a distinct failure

It is tempting to file this as an ordinary bug in a check. It isn't, and the distinction is what
makes it worth a rule.

A broken check gives wrong answers. This check gave *no* answer, and no answer is indistinguishable
from "nothing to report." A monitor that has never alarmed looks identical whether it is watching
carefully or watching nothing at all. **It fails into silence, and silence is what it is supposed to
mean by "fine."**

Worse, it accrues confidence over time. Every quiet day is read as evidence the system is healthy,
when it is evidence of nothing whatsoever.

## The shape, stated generally

**A detector for absence cannot be driven by the events whose absence it detects.**

Once named, we found it in three more places in our own stack:

- **A boundary notification as a liveness signal.** It reports at the end of each unit of work.
  A process that dies mid-unit never reaches a boundary, so the last thing anyone sees is a
  perfectly normal report — and then nothing, forever, which looks the same as idle.
- **A check committed but never registered to run.** It existed in the repository, was written
  carefully, and was cited in review as coverage. Nothing invoked it. It could not fail.
- **A cleanup routine that only ran on graceful shutdown.** The failure mode it was written for was
  ungraceful shutdown.

Same shape every time: **the trigger is a member of the healthy path.** The failure being watched for
removes the trigger.

## The rule

> **Anything that detects "nothing happened" must be driven by a clock, not by the thing that
> stopped happening.**

A timer does not care why nothing arrived. It asks the only question that separates paused from
dead: *how long since the last sign of life?* That question cannot be asked by the sign of life.

Concretely, the split we ended up with:

- The event-driven hook **records state and a timestamp**. It never judges.
- A separate timer **reads that timestamp** on its own schedule and decides. It is the only thing
  permitted to say "stalled."

The hook now has one job it cannot fail at: writing down what it saw. Judgement moved to the only
component that keeps running when everything else stops.

## The test that would have caught it in thirty seconds

Before trusting any monitor, ask:

> **What event drives this? Is that event still present during the failure it's meant to catch?**

If the answer is no — or "not sure" — the monitor cannot see that failure. Ours took one sentence to
answer and we never asked it, because the detector *worked* in testing. It worked because we tested
it against a stalled **state**, which we could construct by hand, rather than against a stalled
**session**, which requires waiting for nothing to happen.

That gap is the whole lesson: **we tested the classifier and never tested the trigger.**

## Why agents make this sharper

An agent asked to "detect when the builder stalls" will reach for the hook that already exists,
because it is the natural place for it and it is right there. That is competent engineering — the
classification logic it wrote was correct, and it passed its tests.

The error is one level up, in a question nobody posed: *is this component reachable during the
condition we are describing?* An agent writing both the detector and its test will construct the test
from the same mental model that chose the hook, so the test inherits the assumption rather than
challenging it.

This is the same reason a green suite is not evidence: **the test and the code share an author, and
therefore share a blind spot.** Here the blind spot was not in either artifact. It was in the wiring
between them, which neither artifact describes.

## The cheap version

For every alarm you rely on, write down the event that fires it. Then write down the failure it is
meant to catch. If the failure would prevent the event, you do not have an alarm — **you have a
component that will be quiet in exactly the situation you built it for.**

Then go one step further and prove it, because a monitor nobody has watched fire is indistinguishable
from one that cannot. Make the thing stop, and wait. If nothing arrives, you have learned something
far cheaper than you will learn it later.
