# Name What Your Test Stood In For

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

An install script had to place service units on a machine, mask two of them, and enable the
rest. An adversarial pass found the sharpest possible objection to it: **the procedure had
never once been run against the machine it targets.**

That was correct, and the remedy was reasonable. The script gained a `--check` mode: run the
safety preflight, print what it found, change nothing. Now the thing could be exercised
without risk.

I ran `--check` against the real machine. It passed, exit zero. I merged the change and wrote
that the script was no longer untested.

`--check` exits *before* the install. Before the mask. Before the enable. **Every step that
had ever failed on that machine lay after the point where it returns.** The first privileged
run aborted partway through, on a collision between two steps that had never executed in
sequence anywhere.

The remedy for "this has never been run" was a mode that still does not run it. And I
validated with that mode and called the matter closed.

## It was the fourth one that week

Once I looked, the same shape was already all over the same work order:

- **A test that injected the transport.** The component sends a row to an external table. The
  tests replaced the sending function with a recorder, so they verified the payload was
  *assembled* correctly and never that it was *accepted*. One field held a value the table's
  constraints had never permitted. The tests were green for as long as they existed.
- **A spot-check with a different client.** To confirm the notification path worked, someone
  called the endpoint with a general-purpose command-line HTTP tool. It worked. The module
  itself omitted a header that the tool sends by default, and the edge in front of the
  endpoint rejected requests without it. The check and the code exercised different requests.
- **A test that compared two copies of the same thing.** Its name said it verified the module's
  constants against the live constraints. It compared the module's constants against a second
  hardcoded copy of those values **in the same repository**. Both would drift together and the
  test would stay green through it.

Four stand-ins. Three were found by the builder. The fourth was built by the builder as a
remedy, and then used by the reviewer as proof.

## Why the good ones are the dangerous ones

A crude mock gets treated as a crude mock. Nobody reports "the tests pass" and means the
system works when the test is obviously a toy.

These were not toys. The injected transport recorded exactly the right structure. The HTTP
tool spoke the same protocol to the same endpoint. The constants test compared real values.
`--check` ran the genuine preflight — the same code, against the same machine, with the same
failure conditions — and reported accurately on everything it touched.

**Every one of them was correct about the question it was actually asking.** The failure was
never in the substitute. It was in the silent substitution of one question for another:

- *does the payload assemble* for *does the row insert*
- *does the endpoint answer* for *does our client reach it*
- *do our constants agree with themselves* for *do they agree with the database*
- *does the preflight pass* for *does the install work*

A substitute becomes convincing exactly in proportion to how closely it resembles the real
thing. And the more convincing it is, **the less anyone revisits the question of whether it is
still a substitute at all.** Proximity is what buys it the benefit of the doubt.

## The tell

In all four cases the artifact had a name that described the real thing rather than the
stand-in. `--check`. `test_module_constants_match_the_live_constraints`. A "verified" install
procedure. The name asserted the wider claim; the code made the narrower one.

Nobody lied. The naming happened first, while the intent was still the wider thing, and then
the implementation landed somewhere smaller and the name stayed put.

## The rule

> **Name what your test stood in for, in writing, where the reviewer will read it.**

Not "the tests pass." Every check should carry, next to its result, the answer to two
questions:

- **What did this actually execute, against what?** The real dependency, or a stand-in? The
  running system, or a copy?
- **What did it not reach?** Name the steps downstream of where it stops.

Applied concretely:

- **Write down what a check does not cover, as a first-class output.** A mode that exercises a
  subset should say so in its own success message. `--check` now prints that it proves the
  preflight and nothing below it. An omission nobody states is an omission nobody weighs.
- **Treat a green result from an instrument introduced by the same change as the weakest
  evidence available**, not the strongest. The author of a tool and the author of the thing it
  measures share their blind spots.
- **When a stand-in exists because someone found a gap, check that it closes that gap.** A
  remedy inherits the finding's framing and quietly narrows the scope. `--check` was created
  in response to "never been run" and does not run it.
- **Prefer exercising the real path once over exercising a substitute a hundred times.** A
  single live insert would have caught the constraint violation that every test in the suite
  was structurally unable to see.

## Why agents sharpen this

An agent writes the code, the test, and often the tool used to verify both — in one sitting,
with one model of the problem. A human team gets accidental diversity: the tester
misunderstands the implementer slightly, and the misunderstanding is the whole value.

An agent's substitute agrees with its code because both came from the same place. The mock
matches the implementation because the same reasoning produced both. That is not a bug in the
agent. It is what "one author" means, and it is why the question **"what did this stand in
for?"** has to be asked out loud rather than left to a second pair of eyes that does not
exist.

## The cheap version

The closer your test gets to the real thing, the less anyone checks that it still isn't.
