# A Goal Must End Where the Agent's Authority Ends

*Field notes from building with AI agents. One failure, one rule.*

> **Note:** this one is about **orchestration** rather than systems — how an agent is
> instructed, not how a program behaves. See *Orchestration* in the index for why that
> distinction is marked rather than smoothed over.

---

## The incident

A builder agent was given a persistent backstop goal: a short description of the desired end
state, re-checked whenever the agent stopped, so the objective would survive after the
detailed instructions scrolled out of its context.

The goal described six outcomes. Four the agent could do. **Two required merging a pull
request and running a privileged install** — and both were forbidden to it, explicitly, in its
own standing instructions. It does not merge its own work. It does not run privileged steps;
it directs the human who does.

The agent did everything it was allowed to do, parked the work for review, and reported
blocked.

The completion hook fired. Zero of six outcomes met. It re-invoked the agent.

The agent explained, correctly, that it was blocked on a human. The hook fired again. And
again. **Nine consecutive invocations across forty-four minutes**, each one accurately
observing that the goal was unmet, each one producing another near-identical status report,
until a human noticed and killed the loop by hand.

Nothing malfunctioned. The agent obeyed its restrictions. The hook evaluated its condition
correctly every single time. The goal was simply **unreachable by construction**, and no
component had any way to know it.

## Why it could not resolve itself

The loop had no vocabulary for the distinction that mattered.

*Goal unmet* covers two entirely different situations:

- **incomplete through inaction** — the agent can still do something; re-invoking is right
- **blocked on an external authority** — the agent cannot do anything; re-invoking is pure cost

A completion check evaluating end state sees the same thing in both cases. The agent's own
report contained the distinction, in plain language, nine times over — but the report is text
and the hook reads a condition.

The agent's own diagnosis was the clearest statement of it: *a goal condition required an
action the model is instructed not to take.*

## It is a permission bug wearing a goal's clothes

The tempting fix is to make the loop smarter — detect repetition, add an attempt cap, teach the
hook to recognise a blocked report. All are worth having, and none address the cause.

The cause is that **two systems of constraint were written separately and never checked
against each other.** The permissions said *you may not merge.* The goal said *be in a state
where it is merged.* Each was correct in isolation. Their conjunction describes a state the
agent is required to reach and forbidden to produce.

That is not a loop bug. It is an unsatisfiable specification, and the loop is just where it
became visible.

A cap would have made it cheaper. It would not have made the goal reachable, and the work
still would not have been done.

## The rule

> **A goal must describe a state the agent can reach using only actions it is permitted to
> take. Where completion requires another party, the goal terminates at the handoff.**

- Wrong: *"…is merged and installed."*
- Right: *"…is authored, adversarially reviewed, and **parked for the gate**."*

The test, applied before any goal is set:

> **Can this agent, acting alone and within its permissions, make this true?**

If no, split it. An agent-scoped goal that closes at the boundary, and a human-owned item
tracked somewhere the agent is not being measured against.

Supporting practices, none of which substitute for the above:

- **Read the goal and the permissions together, once, out loud.** They are usually written at
  different times by different people and never placed side by side. Five seconds of reading
  them as one document catches this class entirely.
- **Make "blocked" a terminal state the loop understands**, not a flavour of incomplete. An
  agent that has correctly stopped should be able to say so in a form the orchestration reads.
- **Cap the re-invocations anyway.** It converts an unbounded failure into a bounded one, which
  is worth having even though it fixes nothing.
- **Be most careful where the boundary is deliberate.** These goals get written in the flush of
  wanting the whole thing done, and the last two items are exactly the ones a human kept for
  themselves on purpose.

## Why agents sharpen this

A human handed an impossible instruction pushes back once and stops. The friction is the
safety mechanism: people do not re-attempt a blocked task nine times in forty-four minutes,
because being stuck feels like something.

An agent in a loop has no such signal. It re-reads the objective, reasons carefully, reaches
the same correct conclusion, reports it clearly, and is immediately asked again. It behaved
well nine times. Diligence with no fatigue is exactly what makes an unsatisfiable goal expensive
instead of self-limiting — every mechanism worked as designed, and the cost accumulated anyway.

The more reliably an agent obeys its restrictions, the more completely a goal that contradicts
them will consume it.

## The cheap version

Never set a goal that can only be met by an action the agent is forbidden to take.
