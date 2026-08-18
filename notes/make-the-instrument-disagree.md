# Make the Instrument Disagree With Itself

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

We needed to know whether a hosted identity provider would bind a token to the specific resource that
requested it, or issue one credential good everywhere. It matters: one is a boundary between machines,
the other is a single key to all of them.

So we probed it. Resource A: rejected. Resource B: rejected. Conclusion drafted — **it can't do it.**

Then someone ran the probe against a resource that *definitely didn't exist*, as a control.

Same rejection. Identical error.

The probe was broken. It had been answering the same thing to every question, and two of those
answers had already been written down as findings.

## Why this is worse than a wrong answer

A wrong answer is a coin flip. **An instrument that returns one value regardless of input has zero
information content** — and it will happily agree with whatever you already suspected.

That's the dangerous property. We *expected* the rejection. The probe confirmed it. Confirmation felt
like evidence, and it was the absence of evidence wearing evidence's clothes.

Read literally, that probe was about to hand a significant architectural decision to the wrong option
on the strength of a broken measurement.

## We had already done this three other ways

Once we named it, the same shape turned up everywhere in our own logs:

- **A digest that was the SHA-256 of empty input.** A before-and-after comparison "matched" perfectly. It was comparing nothing to nothing.
- **Two file-reading checks that both reported a config reload had worked.** It hadn't. They agreed with each other because they were reading the same file, and neither was reading the running process.
- **A test that killed a mock and watched it die**, concluding the real service would also die. The real service survived — different runtime, different signal handling — so the "already fails safe" conclusion was exactly backwards.

Four instruments. Four confident, wrong answers. **None of them was a bug in the thing being tested.**

## The rule

> **Require an instrument to disagree with itself before believing it.**

Before you trust a probe, feed it something it *must* reject and something it *must* accept. If it
answers the same to both, it has told you nothing — regardless of how reasonable its answer looked.

In practice, three questions:

1. **What input would make this report the opposite?** If you can't name one, you don't have a test.
2. **Have I seen it report that opposite?** Not "would it" — *have you watched it go red.*
3. **Is my control genuinely different**, or does it differ in a way the instrument can't perceive?

The third one is subtle and it's where the empty-digest case lived: the control *was* different, but
the instrument was measuring a property that erased the difference.

## The corollary that costs nothing

**Ship the negative case with the test.** Not a comment saying it can fail — a test that reconstructs
the broken condition and asserts the checker rejects it.

We now write these as a pair: `test_the_check_accepts_the_fixed_behaviour` alongside
`test_the_check_REJECTS_the_old_behaviour`. The second one is the one that means something. It's the
difference between a guard and a decoration, and it costs about six lines.

## Why agents make this sharper

An agent writing a probe will make it work on the case you described. That's the case you gave it —
and a probe that returns the expected answer for the expected input looks finished.

Nothing in the request says *"and prove it can return the other answer."* So nobody builds the control,
and the first time the instrument is wrong is the first time it matters.

The one instruction that has caught the most for us, across many sessions: **prove the rejection, not
the issuance.** Anyone can show a thing working. Show me it refusing.

## The cheap version

If you take one thing:

**Run your check against a case that must fail. If it passes, you learned nothing today — including everything it told you earlier.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with AI
agents as builders and a human gate on every merge. Published because the failures repeat, and
naming them makes them visible.*
