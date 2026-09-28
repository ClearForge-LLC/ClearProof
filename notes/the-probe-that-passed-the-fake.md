# Test the Instrument Against the Original Incident

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A styling defect had shipped: a form was supposed to be hidden by the `hidden` attribute,
and it never was. An author rule set `display` on its class, and an author rule beats the
browser's own `[hidden] { display: none }`. So a control the code believed it was hiding
sat visible, full height, in every state where it should have been gone. **A test was green
about it the whole time** — it asserted that the hiding *call* appeared in the page. The
call did appear. It just had no effect.

The lesson looked obvious: the test suite had no way to observe *rendered* behaviour, only
source text. So we added a DOM library, specifically so a test could construct the page and
ask what was actually visible.

The first candidate was rejected in minutes — it had no computed styles at all. Easy.

The second had them, and behaved correctly on every check we threw at it. We adopted it.

Then, almost as an afterthought, someone pointed it at **the original defect**.

It answered `none`.

A real browser answers with the author's value — that disagreement *is* the bug. **The
instrument we had just installed to catch this class of defect would have been green about
the exact defect that caused us to install it.**

## What made it invisible

The synthetic checks we validated it against were all cases where the library and a browser
agree. That is most cases. The library's weakness is narrow and specific: it does not fully
model the precedence between the browser's own stylesheet and the page's. Nothing about
"can it compute styles?" reaches that question, and "can it compute styles?" is the question
we asked.

**We tested the instrument's capability. We did not test its verdict on the thing we cared
about.** Those feel like the same act and they are not. Capability is about the tool.
Verdict is about the tool *and* the case, and only the second one is evidence.

There is a prior rule in this collection — *before you trust a probe, feed it something it
must reject* — and we followed it. We fed it several things it must reject, and it rejected
them. **That rule is necessary and it was not sufficient**, because we chose the rejections
ourselves, and we chose them from the same understanding that had already missed the bug.

## What we did instead

We stopped asking the instrument that question, and replaced the claim with one that can be
checked without it: **every class that sets `display` and is ever toggled by `hidden` must
carry its own `[hidden]` companion rule.** That is a property of the stylesheet and the
markup. No rendering required, no library's judgement involved.

It is enforced by a scan rather than a list — derive the display-setting classes from the
stylesheet, derive the toggled elements from the markup, and require the pairing. A list of
the twelve we knew about would have gone stale at the thirteenth.

**And the scan was born blind to the one case it existed for.** The offending rule was
preceded by a long comment block; a naive match swallowed the comment into the selector, so
that class was never seen. Every other class was found. The scan reported clean.

It was caught by a positive control asserting the scan finds that specific class — written
because the replacement deserved the same suspicion as the thing it replaced.

## The rule

> **Before you trust a new instrument, run it against the incident that made you build it —
> not against a case you invented. A probe can reject every failure you imagine and still be
> blind to the one that actually happened.**

In practice:

- **Keep the original failure as a fixture.** Not a description of it, not a simplified
  version — the real input, the real configuration, the real file. It is the only test case
  you know the instrument must not pass.
- **Separate capability from verdict.** *Can it measure this?* and *does it get this case
  right?* are different questions, and only the second is evidence about your defect.
- **When the instrument is wrong about your case, do not narrow the case.** Replace the
  claim with something checkable by other means. An invariant over source you already have
  beats a rendered measurement you cannot trust.
- **Give the replacement the same suspicion.** Ours was silently blind to the exact class it
  existed for, and only a positive control found it.

## Why agents sharpen this

An agent asked to make a defect testable will reach for the standard instrument, validate it
the standard way, and report honestly that it works — because by the questions asked, it
does. The reasoning that picked the validation cases is the same reasoning that wrote the
code, so the blind spot is inherited rather than detected.

The correction is cheap and mechanical, which is the argument for making it a rule: **the
incident is already written down. Point the new instrument at it before believing anything
else it says.**

## The cheap version

**Your new test can pass a fake failure and miss the real one. Run it against the actual
bug, or you have measured nothing.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with
AI agents as builders and a human gate on every merge. Published because the failures repeat,
and naming them makes them visible.*
