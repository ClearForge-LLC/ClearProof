# The Mutation That Didn't Happen

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A ruling had just landed: one API path was now forbidden, because it silently returned a subset of
what we needed and had already cost us a badly incomplete backup. The lock was written, the tests
were green, and the reviewer asked for the one thing that actually proves a control: **break it on
purpose and watch it fail.**

So I did. I edited the forbidden path back into the source, ran the job, and it came back green.

Green. The lock had not fired.

I was seconds from reporting that the highest-severity control in the system did not work, when I
checked what my edit had actually changed. It had changed three docstrings and a comment. The real
call site read its path from configuration, which my find-and-replace never touched.

**I had mutated documentation and read the unchanged result as a finding.**

## It was not the first time that week

Once I looked, the same shape was everywhere in my own trail:

- **A restore that restored nothing.** I recovered two deleted sections from the upstream branch — and my script asserted they were present before using them, which felt rigorous. The fetch had failed for want of a credential, so the local reference was stale, and the assertion passed by reading a copy of the file from *before* the sections existed. The guard confirmed the bug.
- **Two edits that silently did nothing, twice.** A string replacement anchored on text that existed only on an unmerged branch. No match, no error, no change — the function returns the string either way. I diagnosed this, added assertions to the edits I had just fixed, and left the identical construct unguarded in the same scripts. It failed again the next day for the same reason.
- **A control test with an environment variable that did not exist.** I set an override to point a check at a deliberately wrong target. Three runs came back clean. There was no such variable; every run had used the real configuration and passed correctly.

Five instances, one author, one week. In every case the *interpretation* was careful and the
*mutation* was never verified.

## Why it is worse than a broken test

A broken test gives a wrong answer. This gives **the right answer to a question you did not ask.**

The system under test behaved perfectly every time. Nothing was faulty. The defect lived entirely in
the gap between "I intended to change X" and "X changed" — a gap with no error, no exception, and no
log line, because nothing went wrong. A find-and-replace that matches nothing succeeds. A fetch that
fails leaves the old copy exactly where it was. An unknown environment variable is simply absent.

**Every one of these failure modes is silent by design.** They are the successful outcome of an
operation you did not perform.

And the result is worse than a null: a clean run against an unchanged system looks exactly like a
clean run against a changed one. So it gets *written down as evidence* — evidence for whichever
conclusion you were already leaning toward. Twice I nearly filed a working control as broken. Once I
nearly filed a broken one as working.

## The uncomfortable part

This sits directly downstream of a rule we already had: *before you trust a probe, feed it something
it must reject.* I knew that rule. I was following it. I was in the middle of executing it when it
failed.

Feeding the probe something it must reject requires that **the something actually reaches it.** The
rule assumed the easy half.

## The rule

> **Assert the mutation took effect before you interpret the outcome.**

Not "make the change and observe." Make the change, **prove the change is present in the thing that
will run**, and only then observe.

Concretely, before believing any negative-control result:

- **Read the mutated value back from the running system**, not from your editor and not from the file you think it loaded. If a config knob exists, use it and echo it. If you edited source, grep the call site — not the file.
- **Verify your edit had a target.** A replacement that matched zero times is a no-op that reports success. Assert the anchor exists, and assert the content changed.
- **Fetch before you assert against remote state.** A local reference is a cached opinion. If the fetch can fail, it will, and the assertion after it will pass for the wrong reason.
- **Prefer a knob you can echo to an edit you have to trust.** A documented override that prints its own value is far harder to fake than a source edit.
- **Treat a clean run under an intended-broken configuration as a red flag about your harness first, and a finding about the system second.** The prior should be that you failed to break it, not that it cannot break.

The tell is uniform: **you expected a change and got silence.** Silence is what both success and
total inaction look like. Only one of them leaves a trace, so go and look for it.
