# The Guard Sits Behind Its Own Exit

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

We had a real gap: an AI builder session would finish work, push it, open a pull request — and the
reviewing session never found out. A green PR sat unclaimed for three hours because the handoff
message hadn't landed and nothing was watching for finished-but-unpicked-up work.

So we wrote a check. List open pull requests, ignore anything under fifteen minutes or with failing
tests, and alert once when something is green, pushed, and unmerged.

We put it in the existing watchdog script. We placed it deliberately — **above** the stall-detection
logic, because that path exits early whenever the builder looks healthy, and a healthy builder is
exactly when an unclaimed PR is most likely. We reasoned about placement. We wrote the reasoning into
a comment.

It never fired.

Between the top of the script and our new check sat one line, from the original stall logic:

```sh
[ "$VERDICT" = "park" ] && exit 0
```

**Park is the state that co-occurs with an unclaimed PR.** The builder finishes, parks, and waits.
The one check written for that situation exited before reaching it — via a guard whose entire purpose
was to say *nothing is wrong here*.

The code was correct. The reasoning was correct. The comment explaining the placement was correct.
The placement was wrong by one line, in the direction that made it useless.

## It was not an isolated slip

Within the same day, on a different codebase, the same shape three more times:

**A tap handler in the long-press branch.** We added a dropdown to a floating UI bar and anchored the
new handler on the first matching pattern in the file. That match belonged to the long-press branch,
which sat above the click branch. The button responded only to a long press. Every subsequent "fix"
went into the same dead branch.

**A gesture narrowed out of existence.** We resolved touch gestures in a handler guarded by
`elif act in ("up", "cancel")`, then narrowed inside it to `elif act == "up"`. A tap ends as `up`. A
long press on that platform ends as `cancel` — the widget consumes it. Taps worked. Every hold fell
through the outer branch and out the bottom, resolving nothing. Three attempted fixes all landed
inside the branch that could not receive the event.

**A whole class of handlers disabled by a sibling feature.** Enabling touch events on a widget
suppressed that widget's click events entirely. Tap, dismiss, and long-press stopped working the
moment drag support was added — and each repair was written into the click branch, which by then
could never fire for that widget.

Four incidents, one shape. In every case the code was syntactically valid, present in the file,
reviewed, and inert.

## Why this is hard to catch

A missing function raises an error. A wrong value produces a wrong result. **Unreachable code produces
nothing at all** — and nothing is indistinguishable from "the condition hasn't happened yet."

Worse, it survives every cheap verification:

- It passes syntax checking.
- It appears in `grep`. You can read it back and confirm it exists.
- It appears in the diff, and a reviewer confirms the logic is right — because it is.
- The process starts cleanly and logs a healthy startup.

We repeatedly reported these fixes as shipped. Each time we had verified *presence* and called it
*function*. The instrument answering was "is the code there," and the question that mattered was
"does the code run."

This is close kin to the failure that recurs throughout this repo — a check that reports success while
measuring the wrong thing — but it is worth its own name, because the usual defence does not help. You
can make the assertion strict, make it fail loudly, make it test the real property; **an assertion that
never executes is unaffected by how good it is.** Rigour applied inside an unreachable branch buys
nothing.

## What we do now

**Prove the line ran. Not that it exists.**

The cheapest version is a log line inside the new branch, exercised once against the real condition.
When we finally added `log("tap while open -> dismiss")` to a handler we had "fixed" twice, the log
was empty — and that emptiness was the first honest evidence we had. A single observed line ended an
hour of confident wrong theory.

For anything guard-shaped, three questions before it ships:

1. **What sits above this, and can any of it exit first?** Trace the early returns between the entry
   point and your code, and ask of each: *is this true in the situation my code exists for?* Our
   watchdog guard was `exit 0` on the exact state we were watching for.
2. **What condition does this run under, and have I seen that condition reach it?** Not "should
   reach" — seen.
3. **Does enabling this feature disable another?** Platform APIs trade off. Touch suppressed click
   and we never asked.

And a habit that costs nothing: **when you patch by pattern-matching, check how many times the
pattern occurs.** Anchoring on the first match put a handler in the wrong branch twice in one day. A
`grep -c` before the edit would have caught both.

---

## The rule

> **Code written for a condition must be reachable *in* that condition — and the only proof of that is
> watching it run. Presence is not execution, and a guard placed behind the exit for its own case is
> worse than no guard: it is a promise the system cannot keep, that reads as kept.**
