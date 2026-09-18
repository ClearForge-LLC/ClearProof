# The Alarm Path Is the Least-Tested Code You Have

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A backup service publishes a row to a shared table after every run, so a separate watcher can
tell whether it is still alive. The row carries a severity. On a successful run the code sends
one value; on a failure it sends another.

The table constrains that column to a fixed set. The success value was in the set. **The
failure value had never been in it.**

So every successful run published cleanly, and every failed run raised an exception — into a
variable that was caught and discarded. The watcher saw a steady stream of healthy rows and
nothing else, which is precisely what it would see if the service were healthy.

The component whose entire purpose is to speak up when something is wrong had **never once
completed that job successfully**, from the day it shipped.

It passed two independent reviews and merged.

## Why nobody saw it

Because the system was working. That is the whole difficulty.

Normal operation exercises the success path thousands of times and the failure path zero
times. A backup that runs every fifteen minutes and fails twice in a hundred and seventy runs
will execute its alarm code roughly once a week — and when it does, the result is a line in a
log that nobody is reading, because nothing appears to be wrong.

So the alarm path is, simultaneously:

- **the least-executed code in the system**, because failure is rare by design, and
- **the most consequential**, because it is the only thing that runs when the rare bad thing
  happens.

Test coverage does not rescue this. The line *was* covered. The test constructed a failure and
asserted the right value was passed to the sender — and the sender was a stand-in, so the
constraint that rejected that value was never consulted. Coverage measured that the line ran.
It could not measure that the line *worked*.

## The shape is general

Once named, it is everywhere:

- **The error branch that has never thrown.** Its message formatting is wrong, or it references
  a variable out of scope, and nobody knows because no production error has reached it.
- **The rollback that has never rolled back.** Written alongside the thing it protects, exercised
  in neither.
- **The failover that has never failed over**, the retry whose backoff arithmetic is wrong, the
  cleanup handler on a path that has never been interrupted.
- **The notification for a condition that has not yet occurred.**

Each is written *at the same time* as the happy path, by the same author, with the same
confidence — and then one of them gets exercised ten thousand times a day and the other never
does. They ship equally tested and they diverge immediately.

Worse, the failure path is where the *awkward* dependencies live. It is the branch that has to
format an error, reach a notification service, write an alert row, acquire a lock it does not
normally hold. It has more integration surface than the happy path and less exercise.

## The uncomfortable part

The success path passing is what *hides* the failure path failing.

If both values had been invalid, the service would have been visibly broken on day one and
fixed in an hour. Because one of them was valid, the component looked healthy in exactly the
way a working one does. **A partially correct alarm is more dangerous than a completely broken
one**, because the working half supplies the reassurance.

## The rule

> **Code that only runs when something is already wrong must be exercised deliberately,
> against its real dependencies, or it is not verified — regardless of coverage.**

Concretely:

- **Make the failure happen, for real, once.** Not a mocked failure: a real one, reaching the
  real dependency. Break the thing on purpose and watch the alarm arrive where a human would
  see it. If it has never been observed arriving, it has not been tested.
- **Ask of every alarm: has this ever fired successfully in production?** If the answer is no or
  nobody knows, treat it as unverified code that happens to be deployed.
- **Be suspicious of any pair where one branch is common and the other is rare.** They were
  written together and only one of them has been sanded by use.
- **Watch for asymmetric validity.** Two constants, two paths, one of them exercised — the
  unexercised one is where the wrong value survives.
- **Failure paths deserve integration tests more than success paths, not less.** The happy path
  has production as its test suite. The failure path has only what you wrote.

## Why agents sharpen this

An agent generating both branches produces two that look equally considered. There is no
tell — no rushed comment, no obvious copy-paste, none of the human signals that a section was
written late and never revisited. Both branches read as carefully as each other.

And an agent writing the test for the failure path will, very reasonably, mock the dependency:
it is faster, hermetic, and does not require breaking anything. That decision is correct for
the success path and quietly fatal for the failure path, because the failure path's whole job
is to successfully reach the outside world at the worst possible moment.

## The cheap version

The code that runs only when things go wrong is the code that has never run.
