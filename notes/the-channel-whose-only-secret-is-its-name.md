# A Public Channel Has No Private Fields

*Field notes from building with AI agents. One failure, one rule.*

---

## The incident

A small commerce system pushes notifications to its operator's phone: a piece sold, an order needs
posting. The transport is a self-hosted push service where a channel is just a path — **anyone who
knows the channel name can read it**, and the name was a guessable contraction of the shop's own.

So the channel was designed as a public surface, and the design was good. Every function that builds
a message takes a **narrow input type with nowhere to put** a buyer's email, address or phone. The
list of field names that may never appear on such an input is **exported as a constant**, so the rule
and the guard that enforces it are one object rather than two that can drift. A test fails if any of
those input shapes ever grows a contact-shaped field. The message body is assembled from a table that
has no contact column at all.

Reviewing that felt like reviewing the boundary.

Then the adversarial pass wrote one line.

The payment webhook's own payload carries the buyer's email — it has to, it is how the receipt gets
sent. The attack aliased that field into a local variable and interpolated it into the notification's
**title**.

Every type was satisfied. No forbidden field name appeared anywhere. The whole test suite was green.
**A buyer's email address went out on a world-readable channel.**

## What made it invisible

A type constrains **where a value may be stored**. It says nothing about **where a string may be
built**. Interpolation needs no field.

And the forbidden-field list — the artifact that looked most like the control — was a rule about
**names**. The leak was about **values**. Every check in the tree was correct, and every one of them
was answering a different question than the one that mattered.

**Where we were wrong, specifically:** we had already published the rule that *a flag that says an
exposure exists is not a control; the thing that bounds it is.* Then we built a type discipline,
gave it a security-sounding vocabulary, put it in a file with a warning banner at the top — and
treated it as the bound. It was a more sophisticated flag.

**Name the luck:** nothing caught this. No test, no type, no review. It was found because the work
order required a deliberate adversarial pass by an agent that had not written the code, and that
agent went looking for a way to smuggle a value past a shape. Had the pass been skipped — and it is
the step most easily skipped, because it arrives at the end when the work already looks done — the
leak would have shipped, and **nothing downstream would ever have reported it.** A message that
arrives correctly is indistinguishable from a message that arrives correctly and says too much.

## The rule

> **A notification channel's confidentiality is a property of the channel, not of the message you
> meant to send. If the channel is public, the control is what the message cannot *contain* — checked
> as bytes, at the last point before the send.**

How to apply it:

- **Ask what the confidentiality actually rests on.** If the answer is "nobody knows the name," the
  channel is public. Write that at the top of the module, as a fact, not a caution.
- **Check values, not names.** Take the sensitive strings from the scope where they exist — the
  object whose presence is the only reason a leak is possible — and assert they do not appear in the
  outgoing bytes. It should not care how a value arrived.
- **Put the check at the send, not at a module boundary.** Anything between the boundary and the
  wire can build a new string.
- **Treat every type-level protection of an egress path as a flag until you have found the thing that
  inspects the payload.** If nothing does, you have a convention.

The generalisation past notifications: this is the shape of every log line, error message, crash
report, analytics event and support-ticket attachment. **All of them are egress, all of them are
assembled by interpolation, and a type system has never stopped one.**

## The cheap version

**Don't ask what your message type permits. Ask what your message bytes say — and diff them against
the values you are protecting.**

---

*One of a series of notes on failures hit while building a hardened infrastructure stack with AI
agents as builders and a human gate on every merge. Published because the failures repeat, and
naming them makes them visible.*
