# ClearProof

**Field notes from building production infrastructure with AI agents.
One failure, one rule.**

Almost nobody publishes their failure trail. Writeups describe the system that worked — which teaches
you what to build, and nothing about what to distrust. So the same handful of mistakes get
rediscovered independently, forever: embarrassing in isolation, invisible in aggregate.

This is the aggregate.

Every note here is a real incident from building a hardened infrastructure stack with AI agents as
builders and a human gate on every merge. Each one is sanitised, reproduced, and reduced to a rule
you can apply to a stack that looks nothing like ours.

## The notes

### Systems

How programs, controls and checks fail.

| Note | The rule |
|---|---|
| [Liveness Is Not Identity](notes/liveness-is-not-identity.md) | A port answering proves something is there. It does not prove it's the thing you deployed. |
| [A Flag Is Not a Control](notes/a-flag-is-not-a-control.md) | A flag that says an exposure exists is not a control. The thing that bounds it is — and it must be inside the hash. |
| [Make the Instrument Disagree With Itself](notes/make-the-instrument-disagree.md) | Before you trust a probe, feed it something it must reject. If it answers the same to both, it has told you nothing. |
| [Absence Needs Its Own Clock](notes/absence-needs-its-own-clock.md) | A detector for "nothing happened" cannot be driven by the thing that stopped happening. It will be quiet in exactly the situation you built it for. |
| [The File Nobody Owns Is the One Everybody Reads](notes/the-file-nobody-owns.md) | The more often a file is read automatically, the less often it is read deliberately. Audit those first. |
| [An Absence Has No Symptom](notes/an-absence-has-no-symptom.md) | A check fires on a wrong value. Nothing fires on a missing one. |
| [The Guard Sits Behind Its Own Exit](notes/behind-its-own-exit.md) | Code written for a condition must be reachable *in* that condition. Presence is not execution. |
| [The Mutation That Didn't Happen](notes/the-mutation-that-didnt-happen.md) | Assert the mutation took effect before you interpret the outcome. A change that matched nothing succeeds silently. |
| [The Gate That Verifies Against the Defect](notes/the-gate-that-checks-the-defect.md) | When a ruling forbids a source, every check that consumed it is now suspect — including the ones enforcing the ruling. |
| [The Artifact That Rotted in Place](notes/the-artifact-that-rotted-in-place.md) | An open change decays against a moving base. Staleness is measured in merges, not days — and the artifact never changes while it rots. |
| [The Tip That Advertised Its Scaffold](notes/the-tip-that-advertised-its-scaffold.md) | Never leave a live pull-request tip on placeholder or loading content. Push atomic restores only. |
| [The Failure That Heals Its Own Symptom](notes/the-failure-that-heals-its-symptom.md) | A recovery path must not clear an alarm it cannot verify. If an operation can stop half-done, the half-done state needs a name of its own. |
| [Name What Your Test Stood In For](notes/the-stand-in-that-looked-like-production.md) | A substitute becomes most convincing as it approaches the real thing — and the closer it gets, the less anyone re-checks that it is still a substitute. |
| [The Alarm Path Is the Least-Tested Code You Have](notes/the-alarm-that-worked-until-it-was-needed.md) | Code that runs only when something is already wrong is the least-exercised and most consequential code you own. The success path passing is what hides it. |

### Orchestration

**A deliberate departure from the rest of this repo.** Every note above is about a program — how code, controls and checks fail. The notes below are about *instructing an agent*: the failure is in the specification handed to it, not in anything it executed. They are marked separately rather than blended in, because the reader who wants systems lessons should be able to tell which is which, and because a repo that quietly widens its own scope is doing the thing this repo exists to warn about.

| Note | The rule |
|---|---|
| [A Goal Must End Where the Agent's Authority Ends](notes/a-goal-it-was-forbidden-to-reach.md) | A goal only reachable through an action the agent is forbidden to take can never be met, and a completion loop will pursue it indefinitely. |

## The pattern underneath

Roughly two-thirds of the interesting failures in our private record are **one bug wearing different
clothes: a check that reported success while measuring the wrong thing.**

A process-matching command that matched its own command line. A word boundary that made a search
structurally unable to find most of what it was looking for. A digest that turned out to be the
SHA-256 of empty input, so a before-and-after comparison "matched" while measuring nothing. A mock
that died where the real runtime survived, producing exactly the wrong conclusion. Two independent
checks that agreed with each other and were both wrong.

None of those was a bug in the thing being tested. **Every one was a bug in the instrument** — and
every one looked authoritative right up until something unrelated contradicted it.

That's the through-line, and it's why this repo is called what it is: **the difference between a claim
and a proof.**

There is a second class underneath it, and it is quieter: **a check fires on a wrong value, and
nothing fires on a missing one.** A specification that enumerated nine fields while its own reference
implementation hashed ten, and never mentioned the tenth. A convention that stopped being followed for
twenty-five consecutive units of work while the planning documents kept citing it — unnoticed because
the *outputs* kept arriving on schedule, so the paper trail looked complete from outside. Neither
artifact stated anything false. Both were merely incomplete, and incompleteness produces no symptom.

Every assertion you write is about something that exists. That is why absence is the failure mode a
test suite is structurally blind to.

## Why agents sharpen this

An agent writes the code *and* the check that validates it. Both come from the same understanding of
the problem, so **if that understanding has a hole, the hole is in both.** Corroboration between an
agent's work and an agent's verification of it is not independent evidence — it's the same reasoning,
twice.

Not an argument against agents. An argument for one specific question, asked by a human, about every
green result: *what would make this report success while being wrong?*

## How this repo holds itself to its own standard

The sanitisation gate ([`scripts/check_notes.py`](scripts/check_notes.py)) runs in CI on every push
and pull request. It scans the working tree **and every line ever added in git history** — because a
secret committed once and removed in the next commit is public forever.

And it **runs its own self-test first**, firing every rule against a known-bad sample built at
runtime, before its pass is believed. That's this repo obeying its own third note. A gate nobody has
watched fail is indistinguishable from a gate that cannot.

```
SELF-TEST PASS -- all 13 sanitisation rules fire on a known-bad sample,
the allowlist does not over-match, and the structure check goes red
```

## Reading further

- [`docs/northstar.md`](docs/northstar.md) — why this exists and the five invariants
- [`docs/architecture.md`](docs/architecture.md) — the note format, the gate, and where the raw material lives *(it isn't here, and it isn't copied here)*
- [`docs/roadmap.md`](docs/roadmap.md) — what's published, what's queued

## Licence and use

Take the rules. Use them, argue with them, tell us where they're wrong. If a note saves you an
afternoon, that's the entire point.

---

*Built by [ClearForge LLC](https://github.com/ClearForge-LLC). Notes are curated from a private
incident record; the record stays private, the lessons don't.*
