# The File Nobody Owns Is the One Everybody Reads

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

Coding agents read a primer file at the start of every session — a checked-in document describing the
repo, its conventions, its gotchas. Ours had been doing that faithfully for four weeks.

It opened with this:

> *There is still no package directory, no project file, no lockfile, and no tests.*

The package was in production at the time, serving twenty-six pinned tools on a live device. It had
been for weeks.

The same file also presented a settled architectural decision as an open question, pointed at a
superseded version of our internal security standard, described a retired service as live and in
daily use, and listed a block of commands under *"planned — do not exist yet"* that had existed for a
month. It stated the size of a core hashed structure as one field smaller than it actually was.

Roughly forty merged pull requests separated the file from the repository it described. Every agent
session for four weeks had been primed with it before reading a single line of real code.

## Why nothing caught it

The primer is the one file no unit of work touches.

Change behaviour, you edit code and tests. Change design, you edit the architecture document. Change
sequencing, you edit the roadmap. Every one of those has an owner and a trigger — something in the
work makes you open the file.

The primer describes *the whole*, so it belongs to nothing in particular. It gets written once, at
the beginning, when the repository is empty and the plan is the only content that exists — which
means **it describes intent**, and intent is what a young repo has instead of facts.

Then it freezes, precisely while the repository diverges from its founding state fastest.

And it is auto-loaded, so it has maximum readership and minimum maintenance simultaneously. The
least-updated file in the repo is also the most-read one.

## The measurement that inverted our expectation

We checked five repositories, comparing each primer's last-modified date against its repository's
last commit:

| repo | primer age behind HEAD |
|---|---|
| A | current |
| B | 4 days |
| C | 5 days |
| **D** | **11 days** |
| **E** | **28 days** |

The two stale ones were the two under active heavy build. The three current ones had slow or finished
cadence.

We had assumed the neglected project would hold the stale file. It is the opposite. **Velocity is the
accelerant, not the cure** — because velocity is exactly the rate at which reality departs from a
document that nothing updates.

## Why this bites harder with agents than with people

A new human teammate reads the primer, starts working, and within an hour notices it is wrong. They
build a corrected model and keep it. The document's staleness is absorbed by a person who stays.

An agent session starts cold every time. It reads the primer, believes it, and gets no chance to
accumulate the correction — because the correction lives in a context window that ends.

So a stale primer is not a one-time cost paid by whoever reads it first. It is a **recurring** cost,
paid fresh by every session, forever, in two currencies: tokens spent rediscovering what the file
should have said, and the risk that a confident falsehood goes unchallenged in the one document the
agent has least reason to doubt.

Ours had not caused a visible defect. That was luck, not design — the agent read real files and
self-corrected fast. Luck is not a control.

## The rule

> **The more often a file is read automatically, the less often it is read deliberately.**

Audit those files first. Not the ones you know are neglected — the ones so routinely consumed that
nobody has opened them with intent in months.

Two checks, and you need both:

1. **Mechanical.** Compare the file's last-modified date to the repository's. The gap in days ranks
   your candidates. Cheap, scriptable, and it will surprise you.
2. **Cold read.** Hand the file to someone — or something — with no knowledge of the project and ask
   which statements would mislead them. The gap finds *candidates*; only the cold read finds which
   claims are actually **false**. A file touched last week can still lie.

## The fix is structural, and a cleanup alone guarantees a repeat

We nearly just rewrote it. That would have bought about four weeks.

What the file needed was an **owner and a trigger**, since it had neither:

- **A staleness contract, stated at the top of the file itself:** any change to current state updates
  this document in the same pull request. The reason it rotted is that no step said so.
- **Split the content by decay rate.** Hard-won operational gotchas are durable — keep them. Facts
  about current state either cite the authoritative document or get a verification instruction
  attached.
- **Never restate invariants in the primer.** Cite them by number and point at the authoritative file.
  A second, drifting copy of the rules is the first thing to go stale and the most dangerous when it
  does.

That last one is the general form: **the primer should hold pointers and gotchas, not facts that live
somewhere else.** Every fact it duplicates is a fact that can disagree with its source, silently, in
the document your agents trust most.

## The cheap version

If you take one thing:

**Check the last-modified date of the file your agent reads first. If it predates your last dozen
merges, your agents have been briefed by a stranger describing a project that no longer exists.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with AI
agents as builders and a human gate on every merge. Published because the failures repeat, and
naming them makes them visible.*
