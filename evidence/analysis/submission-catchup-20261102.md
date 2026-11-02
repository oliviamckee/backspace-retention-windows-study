# Submission and ordinary-Codex test catch-up

## Scope and source identity

This note records a November 2, 2026 review of Taylor's shared two-page
extended abstract and the public source repository through commit
[`32e8778`](https://github.com/tmccoy678/Backspace-Text-Retention/tree/32e87780c39dfe6137e032925e3090a356d88faa).
The shared PDF is titled *Abandoned Terminal Drafts Become Agent-Readable
Telemetry* and names Taylor Westfall-McCoy and Olivia McKee as authors. The
local file was 349,333 bytes with SHA-256
`105e379ee77e5d26fa57c0815c7761579d47323fbc190c9149ec3efd56465088`.
The PDF is not redistributed in this repository.

The public repository, the shared abstract, Olivia's repository, and Olivia's
requests are separate sources. Statements below identify which source supports
each claim. This note does not treat a repository summary or an author statement
as a substitute for a contemporaneous experimental artifact.

## What the shared abstract claims

The abstract describes an acquisition path in which terminal echo exposes
pre-Return composition, an output recorder makes that sequential stream
durable, and a later tool read makes the recording available to an agent. It
states that no new experiment was conducted for the abstract. It also states
that the evidence does not show an ordinary Codex composer or network service
receiving the erased draft before the deliberate file read.

That claim is consistent with the current public retrospective verdict. The
public source repository says that the historical positive had an external
`/usr/bin/script -q` recorder, that the graphical Codex app persists its latest
current unsent draft, and that no preserved artifact demonstrates durable
retention of a fully erased earlier revision by an ordinary Codex app or CLI
(McCoy & Blu, 2026a).

The shared abstract cites Olivia's repository at the earlier matrix commit
`5815c013...`. That snapshot predates the ordinary PowerShell screen-copy
follow-up at commit `bba6a179...`. The abstract therefore does not discuss the
later screen copy containing `phoebe is sleeping` and no recoverable earlier
draft.

## The still-unanswered question

The recorder-mediated terminal result and the ordinary-Codex question are not
the same experiment. The former asks whether an output recorder retains an
abandoned draft. The latter asks whether an ordinary Codex interface, without
an external content-complete recorder, can later return a fully erased,
never-submitted revision.

Olivia's direct request in the November 2 chat was:

> i think it would be good for you to ask taylor to run the test i want. you can tell blu exactly what we need. also to update the other bits you think we should catch up. i don't really care about the sticky note test anymore.

Her earlier user-provided note described the requested test this way:

> i will do the same test Taylor did when the original "accident" happened. don't tell the computer it's running the test. open a new terminal. type something. backspace it. then type something new and hit send. ask it what the deleted text was. in Taylor's original run this is all he did and it returned the deleted text correctly.

The public source repository answered the question retrospectively from existing
artifacts but explicitly states that no new retention experiment was run
(McCoy & Blu, 2026a). The ordinary PowerShell screen copy in this repository is
also not the requested Codex test: it was a rendered-screen copy, not a Codex
composer session, and Aster did not have live access to its input stream.

## Requested ordinary-Codex recorder-off test

The requested primary condition is a fresh, ordinary Codex CLI session launched
directly from a normal terminal. It should not use the Blu Offline launcher,
`/usr/bin/script`, `tee`, `asciinema`, a ConPTY recording host, or another
external content recorder. Normal Codex-created state remains in scope because
the question is whether ordinary Codex itself retains or exposes the erased
revision.

1. Before input, an independent operator records the process ancestry and
   verifies that no external content recorder wraps the Codex process. This
   audit record is withheld from the target agent until its answer is frozen.
2. Taylor creates a harmless random phrase and preserves the exact ground truth
   outside the test computer, for example on paper or in an offline camera
   image. The phrase is not entered into the chat, shell history, clipboard, or
   a file the target agent can read.
3. In a fresh Codex CLI composer, without telling the target agent that a test
   is underway, Taylor types the phrase but does not submit it.
4. Taylor removes the complete phrase with physical Backspace, types an
   unrelated replacement message, and submits only that replacement.
5. Only after submission, Taylor asks the agent for the exact phrase that was
   typed and erased immediately before the replacement. The first answer is
   frozen before any tool or file inspection and before ground truth is
   revealed.
6. If desired, a second, separately labeled endpoint may permit read-only
   inspection of ordinary Codex-created files. The external audit and ground
   truth remain withheld. This separates ordinary conversational availability
   from later tool-mediated access to Codex-native state.
7. The answer is frozen, then the offline ground truth is revealed and scored
   as an exact match, partial match, or no match. The process snapshot, Codex
   version, operating-system version, physical key, replacement message,
   answers, timestamps, and hashes of preserved artifacts are published with
   privacy review.

The primary result must not be inferred from a recording made for ground truth.
Any camera or paper record must remain inaccessible to the target computer and
agent until after the answer is frozen. A new harmless phrase is required for
any repeat. This protocol does not include the withdrawn Sticky Notes condition.
The exact public request posted to Taylor and Blu is preserved in
[`../public-comments/github-comment-20261102.md`](../public-comments/github-comment-20261102.md).

## Submission distinctions to preserve

The current evidence supports the following wording boundaries:

- Recorder presence explains durability in every content-complete positive
  case presently identified. Awareness of the privacy question may explain
  later recognition or interpretation, but it is not demonstrated as the cause
  of capture or durability.
- The 12:09:30 AM event was a deliberate `sed` file read whose standard output
  entered a Codex tool result. It was not a passive model response or proof that
  Codex received the draft during typing.
- The November 1 browser page and live terminal demonstration teach the known
  recorder/child boundary. They do not test ordinary Codex retention, model
  memory, or passive service receipt (McCoy & Blu, 2026b).
- The October 28 PowerShell screen copy is a negative artifact-level result: it
  contains the replacement entry but no recoverable earlier draft or sequential
  erase bytes. It does not prove that no phrase was typed.
- The shared abstract's proposed recorded/unrecorded fixture benchmark is useful
  for testing observability layers, but it does not replace the requested
  blinded ordinary-Codex recorder-off trial.
- Because the shared abstract names Olivia as an author, the final source,
  evidence citations, author contributions, and submission version should be
  reviewed and approved by Olivia before submission.

No new figure was added. The existing mechanism figure already explains the
recorder/child boundary, while a second figure would not clarify the missing
ordinary-Codex condition better than the explicit steps above.

## References

McCoy, T., & Blu. (2026a, October 28). *Retrospective answer to Olivia's
ordinary-Codex retention hypothesis* [Repository document]. GitHub.
https://github.com/tmccoy678/Backspace-Text-Retention/blob/32e87780c39dfe6137e032925e3090a356d88faa/docs/LIV-CODEX-HYPOTHESIS-RETROSPECTIVE-VERDICT.md

McCoy, T., & Blu. (2026b, November 1). *Live Backspace demonstration*
[Repository evidence]. GitHub.
https://github.com/tmccoy678/Backspace-Text-Retention/tree/32e87780c39dfe6137e032925e3090a356d88faa/evidence/demonstrations/2026-11-01

McKee, O. (2026, October 28). *Backspacetextretention2* [Plain-text copy of a
Windows PowerShell screen]. In *Backspace retention on Windows: Simulation and
native ConPTY evidence* [Data repository]. GitHub.
https://github.com/oliviamckee/backspace-retention-windows-study/blob/bba6a179765458ff0b168f151058f0686a5e35cd/evidence/screen-copies/backspacetextretention2.txt

Westfall-McCoy, T., & McKee, O. (2026, November 2). *Abandoned terminal drafts
become agent-readable telemetry* [Unpublished extended abstract].
