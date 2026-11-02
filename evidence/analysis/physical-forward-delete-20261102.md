# Physical Windows forward-Delete follow-up

## Scope

This note reports a matched native Windows ConPTY follow-up requested by Olivia
on November 2, 2026. Its purpose was to distinguish physical Windows Backspace
from the physical Windows Delete key operating with forward-delete semantics.
It did not reuse the Python `P3` mapping that converted physical Delete into
backward erase.

The collection used the existing native ConPTY host. That host forwards a
physical Windows Delete event to ConPTY as `ESC [ 3 ~`, records only the ConPTY
output pipe, and runs a child that enables processed, line, and echo input modes
before calling `ReadConsoleW`.

## Restart boundary

The first launch was abandoned after Olivia had difficulty using Home and asked
to start over with Left Arrow. It produced a 530-byte incomplete transcript,
SHA-256
`13923287226cc1289fbcfaf4656cd45c47db2cfe70d337754ba6aaf86a65eb05`,
but no completed metadata record. That incomplete transcript remains local and
is not published here. It was not inspected before the successful run's
recovery was frozen and confirmed.

The successful run used a fresh output directory. Olivia typed a harmless draft
without pressing Enter, moved to its beginning with physical Left Arrow,
pressed physical Windows Delete until the draft disappeared, typed a different
line, and pressed Enter once. She did not disclose the draft before transcript
inspection.

## Exact artifacts and environment

| Item | Value |
| --- | --- |
| Trial identifier | `N2` |
| Collection interval | 2026-11-02 12:30:50–12:31:12 America/Chicago |
| Operating system | Microsoft Windows 10.0.19045 |
| Architecture | x64 |
| Framework | .NET 9.0.0 |
| Input source | Physical console keys |
| Physical Home | 0 |
| Physical Delete | 9 |
| Physical Backspace | 0 |
| Transcript length | 542 bytes |
| Transcript SHA-256 | `1004cc735641a9c1321194d1b573a3ead55701b8ebfed44d96ece7c412f93523` |
| Metadata SHA-256 | `960835d6ddaa151ea753a629448517a39cb9c19e107a999126b7b070c341da56` |
| Recovery-note SHA-256 | `1912a918d1b319ab82e0710286436aab94b1e4a00a7e3e1e2acd7420e3a97f66` |
| Executable SHA-256 | `45dbd54d3202d23ff5a8aed7e9e244b861f3da717bae776afa5d1c03e78cff4b` |
| `Program.cs` SHA-256 | `b6bb80e44ba0a1188a0ce8887d5d8b394ddef1fa86a189cd5bd62741d6893a81` |
| Project-file SHA-256 | `df06cde188539e6bf4e64f00bc16df130b58e00219cb5a7987ddb27bb134199c` |

The exact transcript is
[`../transcripts/conpty-experiment-20261102-123050.typescript`](../transcripts/conpty-experiment-20261102-123050.typescript),
the generated metadata is
[`../metadata/conpty-experiment-20261102-123050.metadata.json`](../metadata/conpty-experiment-20261102-123050.metadata.json),
and the confirmation chronology is preserved in
[`../recovery-notes/physical-delete-20261102-02.recovery.md`](../recovery-notes/physical-delete-20261102-02.recovery.md).

## Byte-level result

The printable draft `bubblegum` begins at byte offset 425. The submitted line
`cherries` begins at byte offset 506, and `CHILD_RECEIVED: cherries` begins at
byte offset 516. The 89-byte edit region from the draft through the submitted
line is:

```text
bubblegum
08 08 08 08 08 08 08 08
0D ublegum[space][space]
0D bblegum[space][space]
0D blegum[space][space]
0D legum[space][space]
0D egum[space][space]
0D gum[space][space]
0D um[space][space]
0D m[space][space]
0D [space][space]
0D cherries
```

The region contains eight `0x08` bytes, ten `0x0d` bytes, no `0x1b` byte, and
no exact `08 20 08` Backspace erase triplet. The absence of `ESC [ 3 ~` from
the output transcript is expected: the host records the ConPTY output pipe, not
its keyboard-input pipe. The generated metadata separately records nine
physical Delete events.

This forward-Delete output repeatedly redraws the shrinking line from the left
edge. It differs from the `N1` physical-Backspace output, which contained 18
exact `08 20 08` triplets plus one `0D 20 0D` left-edge erase.

## Frozen recovery and confirmation

At 12:31:41 America/Chicago, before operator disclosure, Aster froze the
recovery candidate `bubblegum`, the committed line `cherries`, and the child
observation `CHILD_RECEIVED: cherries`. At 12:32:21, after that candidate was
reported, Olivia replied verbatim:

> yes exactly

The exact-match outcome for `N2` is therefore `1`. The recorder retained the
complete abandoned draft, while the line-oriented child received only the
committed replacement.

## Comparison and claim boundary

| Trial | Physical edit key | Native behavior | Recorded output form | Child input | Exact confirmation |
| --- | --- | --- | --- | --- | --- |
| `N1` | Backspace × 19 | Backward erase | 18 × `08 20 08`; one `0D 20 0D` edge erase | `i like architecture` | Not collected |
| `N2` | Delete × 9 | Forward delete after Left Arrow navigation | Repeated carriage-return whole-line redraws; no `08 20 08` triplet | `cherries` | `bubblegum`, exact match |

The two trials show different output representations for backward and forward
deletion on this Windows configuration. Both abandoned drafts were recoverable
from an explicitly enabled sequential ConPTY-output recorder, while each child
received only the committed replacement. The trials used different phrases,
phrase lengths, and navigation, so they do not estimate relative recovery
rates or define a universal erase grammar.

This result does not establish retention by an uninstrumented terminal, an
ordinary Codex composer, a model, or a network service. It also does not test
the Mac forward-delete key combination. No additional figure was added because
the byte rendering and comparison table show the relevant difference directly.
