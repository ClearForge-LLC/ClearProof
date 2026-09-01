# An Absence Has No Symptom

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

Our internal security standard defines the canonical object that gets hashed into an integrity
manifest. It enumerates the fields, and it carries this rule in its own text:

> *This enumeration and the executable form must list the same set; if they diverge, the executable
> form is authoritative and this list is the bug.*

The standard enumerated nine fields and asserted **"Nine fields."**

The reference implementation had been hashing **ten** for a week. The tenth field had been invented
there, deliberately, because a control the standard assumed — containing a process by caging its
network egress — turned out to be unreachable on that platform. So the node built a different
mechanism to do the same job, and it worked, and it graduated seven previously-blocked capabilities.

The standard did not mention that field once. Not in the enumeration, not in prose, not anywhere.

By the standard's own rule, the standard was the bug. It had been the bug for seven days, and it was
caught only because an unrelated documentation-reconciliation task happened to have both artifacts
open at the same time.

## The rule that named the failure and detected nothing

Read that quoted rule again. It anticipates the exact failure. It assigns authority correctly. It
tells you which side to fix.

**Nothing ran.** There was no test comparing the written enumeration to the executable form, because
such a test spans two repositories and therefore belongs to neither.

A sentence in a document that says *"these two must agree"* is a comment. It is indistinguishable
from a control right up until the moment they disagree — and then it is indistinguishable from
nothing at all.

## Why this direction of drift is invisible

Ordinary documentation rot is **the document claiming something the code does not do**. Anyone
reading the two together sees a false statement. It is embarrassing, and it is *findable*.

This was the other direction: **the code doing something the document did not know about.**

The standard made no false claim. Every sentence in it was true. It was merely **incomplete** — and
incompleteness produces no failing test, no drift alert, no contradiction, no symptom of any kind.
Both artifacts were internally consistent. Both suites were green. Only the *relationship* between
them was broken, and nothing tests a relationship that spans two owners.

You cannot grep for a sentence that was never written.

## It happened twice that week, in a different disguise

The same class produced a second finding days later, and the second one is the better teacher because
nothing about it looks like a security problem.

Our work orders live in a specific directory, one file per order. The planning documents cite that
path throughout. It is a settled convention with over a hundred files behind it.

It had **silently stopped being followed five weeks earlier.** Roughly twenty-five consecutive work
orders were never committed there. Some sat misfiled elsewhere; ten had never been committed at all
and survived only as loose files on a build machine. One disk failure would have taken twenty-five
contracts with them.

Nobody noticed, and here is the part worth sitting with: **the reports kept arriving on schedule.**
Every order produced its output document, filed correctly, on time. From outside, the paper trail
looked complete. The *contract* those reports answered to had quietly become ephemeral while the
*evidence* of work stayed pristine.

And it had a downstream cost we had misdiagnosed as a style problem. With no durable order in the
repository, the chat message that started each build session **became** the work order — so those
messages grew, absorbing scope that should have lived in a file, until they were restating whole
sections back at the builder. We had been treating that as verbosity. It was a missing artifact.

## The rule

> **A check fires on a wrong value. Nothing fires on a missing one.**

Its companion is [Absence Needs Its Own Clock](absence-needs-its-own-clock.md): what to do once you
*have* written the detector, and why wiring it to the wrong trigger leaves you exactly as blind.

Absence is the failure mode your test suite is structurally blind to, because every assertion you
write is about something that exists.

Three questions that surface it:

1. **Search your specs for their own consistency claims.** Every sentence of the form *"these must
   agree"*, *"X is authoritative"*, *"this list must match"* is a latent instance. For each one ask:
   **what runs?** If the answer is "a careful reader", you have a comment.
2. **Ask what is supposed to exist, not just whether what exists is correct.** Convention compliance
   is an absence question — *is there a file here?* — and nothing in a normal gate asks it.
3. **When two artifacts must agree and live under different owners, the check belongs to whichever
   side can see both.** Usually the implementation, which already imports the executable form. Absent
   that assignment, the check is nobody's, which is how it never gets written.

## The feedback path is part of the standard, not a courtesy

There is a specific version of this worth naming, because it compounds.

Everyone builds the path from standard **down** to implementation: port it, don't reinvent it. Almost
nobody builds the path from implementation back **up**.

So the reference node — the one actually meeting reality, the one that discovers the cage does not
hold on this platform — advances, and the standard does not. Then the *next* node ports from the
standard, finds the mechanism missing, and reinvents it. Now two implementations solve the same
problem differently, with no record of which was right, and **the second one is the one nobody
audited.**

We got our week's grace by luck: our standard has a rule that a version stays mutable until its first
adoption, and the adopting change had not merged yet. Had it landed an hour earlier, a known-wrong
enumeration would have frozen into the standard for an entire version. **That was a window, not a
design.**

If a mechanism gets invented at a reference node, the upstream amendment lands in the *same* unit of
work. A follow-up item is where it dies.

## Why agents sharpen this

An agent asked to make a document correct will fix every statement in it. That is what "correct"
means to a reader, and both a human and an agent will do it well.

Neither will reliably notice the paragraph that was never written — and an agent has a specific
disadvantage here, because it works from what is in front of it. The missing thing is, definitionally,
not in front of it.

The instruction that has worked for us is not *"check this document is accurate."* It is: **"list
what this document should contain and does not."** Those are different requests, and only the second
one can find an absence.

## The cheap version

If you take one thing:

**Grep your specs for the phrase "must match." For each hit, ask what executes. If the answer is a
careful reader, you have a comment that has been impersonating a control.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with AI
agents as builders and a human gate on every merge. Published because the failures repeat, and
naming them makes them visible.*
