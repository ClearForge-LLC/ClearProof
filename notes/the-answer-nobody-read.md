# A Returned Failure That Every Caller Discards Is a Silent Failure

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A monitoring system sends its most serious alerts — the ones for data loss — through a push
notification service. Each alert carries a short title and a longer body.

Someone improved the titles. Instead of a bare error key, each of the eleven highest-severity
alerts got a human-readable headline: *"CM1 — sentinel MISSING"*, *"CM1 — mirror CORRUPT"*, and
so on. Clearer, more scannable, obviously better.

Every one of those titles contained an **em-dash**.

The title travels in an HTTP header. HTTP headers are `latin-1`. An em-dash is not in
`latin-1`. So from the moment that improvement shipped, **every single one of the eleven
highest-severity alerts in the system was undeliverable.** The most urgent channel — the one
reserved for conditions where waiting for a second occurrence is unacceptable — was dead, and
had been for weeks.

It was found by accident, months later, during an unrelated test.

## The part that should have prevented it

The code was not ignorant of the failure. It caught the encoding error, wrote a line to the
journal reading **`failure-alert NOT delivered:`** with the exception text, and returned
`False`.

**All six call sites discarded the return value.**

Not one of them checked it. The function knew, said so precisely, published a correct and
specific diagnosis — into a journal nobody reads when nothing appears to be wrong, and a
boolean nobody assigned to a variable.

A deliberate mutation was later introduced to test this: change the code so a *lost* alert
reports as *delivered*. The mutant **survived the entire test suite** — 443 tests — because no
test and no caller ever looked at what the function returned.

## Why this is not the usual failure

Most silent failures are silent because the information does not exist. A check that was never
written. A branch that never ran. A probe that could not see the thing it was asked about.

This one is different, and worse in a specific way: **the information existed, was correct, was
complete, and was produced on time.** The system diagnosed itself accurately and then threw the
diagnosis away.

That distinction matters because the two have opposite fixes. Missing information needs a new
check. **Discarded information needs no new knowledge at all** — only that somebody read what
was already being said. Which means the defect can persist indefinitely while every component
behaves exactly as designed.

## The shape, generalised

A function can report failure three ways, and they are not equivalent:

- **It raises.** The caller must handle it or crash. The failure cannot be ignored by accident —
  only deliberately, with a visible `except`.
- **It returns a status.** The caller *may* ignore it, and in practice usually does, because
  ignoring it requires writing nothing at all.
- **It logs.** The failure is recorded where it will be read only by someone already suspicious.

The second is the dangerous one, precisely because it feels responsible. The author of the
function did their job: they detected the condition and reported it. The contract was honoured.
And the reporting mechanism they chose is the one whose default behaviour on the caller's side
is **silence**.

Logging alongside it makes this worse, not better, by supplying the feeling that the failure was
handled. A line in a journal is not an alert; it is an alert you have to already know to go
looking for.

## The rule

> **If a function can fail in a way that only its return value reports, and any caller discards
> that value, the failure is silent. Make it raise, or make discarding it impossible.**

In practice:

- **For anything whose whole purpose is to reach a human — alerts, pages, notifications — prefer
  raising.** A notification that silently fails to send is indistinguishable from a system with
  nothing to report, and that is the exact confusion the notification exists to prevent.
- **Audit call sites, not just functions.** A function returning a meaningful status is only half
  the contract. Grep for every call and ask what it does with the answer. "Nothing" is the
  common case.
- **Mutation-test the reporting path itself.** Change the code so a failure reports as a success.
  If the suite stays green, no test is asserting the thing you most need to be true. A green
  suite over that mutant is not a passing suite; it is a suite that does not test this.
- **Be most suspicious of the cosmetic change to an unexercised path.** Nobody reviews a
  title string. Nobody tests a title string. And a path that only runs during failures will not
  reveal the mistake in normal operation — so the improvement and its consequence ship together,
  untested, and stay that way until something goes wrong badly enough to need them.

## The bitter detail

Before the titles were added, the alerts were deliverable. The improvement broke them.

And there is a second-order consequence worth stating, because it is the kind of thing that
makes an incident hard to reconstruct afterwards: **the one alert of this class anyone ever
received arrived only because it predated the change.** That alert was itself investigated, and
the investigation produced the very commit that added the titles. The fix for one defect
disabled the channel that reported it, and the evidence that the channel had ever worked was
older than the fix.

## Why agents sharpen this

An agent asked to improve alert messages will improve the messages. It is a small, well-scoped,
obviously-beneficial task, and the change is textual — the kind of edit that reads as risk-free
to a reviewer scanning a diff.

The encoding constraint lives in a different file, in a transport layer, expressed as a property
of HTTP rather than of this system. Connecting "I made this string prettier" to "headers are
latin-1" requires holding two unrelated facts at once, and nothing in the task prompts for it.

That is not an agent-specific weakness — a human would miss it identically. What *is*
agent-specific is throughput: an agent makes many such small improvements quickly, each locally
correct, and the surface area for this class of mistake grows with the rate of change rather
than with its difficulty.

## The cheap version

A failure nobody reads is a failure nobody had.
