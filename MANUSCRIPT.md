# Recoverability of visually deleted terminal drafts in instrumented Windows sessions

## Abstract

Terminal interfaces distinguish the text visible during editing from the line
eventually returned to an application. This technical record examined whether
text typed and visually erased on Windows remained recoverable from an
explicitly enabled sequential recorder. Three purpose-built Python-harness
trials and one native Windows Pseudoconsole (ConPTY) trial were completed after
an aborted setup attempt. The native host forwarded physical keyboard input to
ConPTY and recorded only the ConPTY output pipe; a child process enabled
processed, line, and echo input modes and called `ReadConsoleW`. In the native
trial, the operator typed a 19-character draft, erased it with 19 physical
Backspace presses, typed a replacement, and pressed Enter. The transcript
retained the complete abandoned draft followed by 18 `08 20 08` erasures and
one left-edge `0D 20 0D` erasure. The child reported only the committed
replacement. This establishes recovery from the declared Windows ConPTY
recording path and a separation between recorded terminal output and committed
application input. A follow-up four-case native matrix crossed starting column
0 versus 4 with Backspace serialized as `0x7f` versus `0x08`. Column 0 produced
four `08 20 08` erasures plus one `0D 20 0D` edge erasure; column 4 produced
five `08 20 08` erasures. The two input-byte conditions had identical output
within each column pair after normalizing the printed case label. These
observations do not establish independent retention by an
uninstrumented terminal, a message composer, a language model, or a network
service. Because the operator did not separately confirm the recovered drafts
after disclosure, exact agreement with an independent ground-truth record was
not scored.

## Introduction

A terminal display is a rendering of a sequential stream, not a final-state
database. Under canonical or cooked line editing, an operating-system terminal
component can echo characters while a user types, process erasure actions, and
return only the completed line after Enter. A recorder positioned on the echoed
output path can therefore preserve characters that later control operations
remove from the display.

The motivating macOS record described this boundary using `/usr/bin/script`, a
pseudo-terminal, and a local command-line model. Its central claim was limited:
the sequential `.typescript` file retained an abandoned draft and the bytes
that visually erased it, while the application response was consistent with
receipt of only the committed line (McCoy & Blu, 2026). Apple's `script(1)`
manual states that the utility records everything printed on the terminal and
warns that the log contains linefeeds and backspaces (Apple Inc., 2022).

Windows exposes a related but distinct architecture. ConPTY allows a hosting
application to provide input and output streams for a character-mode child,
with the operating system translating between the console API and UTF-8 text
plus virtual-terminal sequences (Microsoft, 2022a, 2022b). Windows console
modes specify that echo input writes characters to the active screen buffer,
line input withholds the line until carriage return, and processed input handles
Backspace, carriage return, and line feed when line input is enabled (Microsoft,
2021, 2023).

The present work documents an iterative Windows reproduction. Its primary
technical question was:

> When an explicitly enabled recorder captures the native Windows ConPTY output
> stream, can a visually erased draft remain in that stream while
> `ReadConsoleW` returns only the committed replacement line?

The work was not preregistered, randomized, or designed to estimate a recovery
rate. It is a transparent engineering record of one sequence of sessions.

## Methods

### Design and evidence policy

The initial work proceeded in two stages. First, a Python harness simulated the
recorder/edit/commit boundary. Second, a native Windows ConPTY host delegated
line editing to the operating system. After public review, a scripted native
follow-up crossed two starting columns with two serialized Backspace bytes.
Every designated evidence `.typescript` file was preserved without conversion.
Contemporaneous JSON metadata and recovery notes were retained, and SHA-256
digests were calculated over the exact bytes.

The operator was instructed to use made-up, nonsensitive English phrases. The
inspector did not receive a phrase in chat before reading the transcript.
However, no separate paper record, cryptographic commitment, or later explicit
operator confirmation established ground truth. Consequently, strings read
from the transcript are reported as **recovery candidates**, not scored exact
matches.

### Source material and environment

The macOS method and claim boundaries were reviewed from
`tmccoy678/Backspace-Text-Retention` at commit
`b3ab71be4269db2754476cc2187b80877945b849` (McCoy & Blu, 2026). The native
Windows implementation followed Microsoft's documented ConPTY session design
and the official MiniTerm sample architecture, inspected at Microsoft Terminal
commit `c91793f7dc022f1a10cacdc7a228ddce63942dc8` (Microsoft, 2025;
Microsoft, n.d.).

The Python metadata identifies Python 3.12.10 on `win32`. The native metadata
identifies Microsoft Windows 10.0.19045, x64, and .NET 9.0.0. No local language
model was downloaded or used. A deterministic receiver replaced the model
because the measured boundary concerned line commitment, not generation.

### Python simulation

The Python harness read console keys directly, maintained an editable buffer,
displayed typed characters, appended `08 20 08` for backward erasures, and
wrote the same byte stream to a transcript. On an accepted Enter event, it
started a separate receiver and sent only the committed line through standard
input. This stage demonstrated the intended data separation but did not measure
native Windows cooked-line behavior because the harness itself implemented the
editing.

The simulation evolved during use:

1. `A0` was aborted when an initially requested terminal panel did not become
   visible.
2. `P1` and `P2` required exact predeclared committed-control lines. The
   operator instead entered replacement English sentences; both trials were
   retained as control mismatches and their receivers were not launched.
3. `P3` accepted any nonempty committed line. The physical Windows Del key was
   explicitly mapped to backward erase by the harness. This mapping reproduced
   the Mac key labeled Delete, but it did not represent native Windows forward-
   Delete semantics.

Only the final v3 Python source was frozen. Earlier output artifacts are exact,
but exact v1 and v2 source snapshots were not preserved and have not been
reconstructed.

### Native Windows ConPTY trial

The native host created synchronous input and output pipes, called
`CreatePseudoConsole`, and attached a child process with the
`PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE` process attribute. Microsoft documents
this pipe-based arrangement as the normal ConPTY hosting model (Microsoft,
2022a, 2022c). One thread copied every byte read from the ConPTY output pipe to
both the visible parent console and a `.typescript` file. The transcript writer
did not consume the host's keyboard-input stream.

The host used `Console.ReadKey(intercept: true)` to collect physical key events
and serialized them to ConPTY input, as a terminal front end must do. For the
reported physical trial, ordinary characters and Backspace were forwarded; no
Home or Del events occurred. The host did not maintain the child's editable
line.

The child enabled `ENABLE_PROCESSED_INPUT`, `ENABLE_LINE_INPUT`, and
`ENABLE_ECHO_INPUT`, then called `ReadConsoleW`. Under these modes, Windows
handles the editing and echo, and `ReadConsoleW` returns after carriage return
(Microsoft, 2021, 2023). After the call returned, the child printed one line
beginning `CHILD_RECEIVED:` followed by the committed value.

Before physical collection, a scripted control sent `alpha`, Home, five forward
Delete sequences, `omega`, and carriage return. The raw ConPTY transcript
contained `alpha`, while the child printed `CHILD_RECEIVED: omega`. This control
was retained as `N0`.

For the physical native trial (`N1`), the operator typed a draft without Enter,
pressed Backspace once per character, typed a replacement, and pressed Enter.
The collection program counted physical key categories and recorded the child
exit code.

### Follow-up Backspace matrix

The follow-up matrix retained the same ConPTY host, output-only recorder,
processed console modes, and `ReadConsoleW` child. It crossed starting column 0
versus 4 with Backspace serialized to ConPTY input as `0x7f` versus `0x08`.
The four-character application-output prefix `>>>>` established column 4. In
each case the host sent `alpha`, five Backspace bytes, `omega`, and carriage
return. A 75 ms delay separated each scripted key so the console emitted
per-key edit output rather than coalescing rapid input into a whole-line redraw.

The matrix was adaptive. An initial noninteractive launch stopped before input
because the parent lacked a console; a second non-PTY launch reached the child
but `GetConsoleMode(stdin)` failed before experimental input. A terminal-attached
pilot without key pacing completed but produced coalesced redraw output. Those
runs were treated as development observations. The designated four-case matrix
was collected after terminal attachment and pacing were fixed. Collection
details are in `provenance/MATRIX_NOTES.md`.

### Inspection and analysis

Inspection was read-only. SHA-256, byte length, literal printable regions, and
erase structures were recorded. The primary native evidence was defined as:

- presence of the abandoned printable draft before erase output;
- physical Backspace count from collection metadata;
- presence and count of exact erase sequences;
- the printable committed line after the erase region;
- the child's `CHILD_RECEIVED:` line; and
- a zero child exit code.

No inferential statistics were calculated. The sessions were sequential,
adaptive, and conducted on one machine with one operator.

## Results

### Trial inventory

| Trial | Mechanism | Collection status | Recovery candidate | Committed line | Receiver/child observation |
| --- | --- | --- | --- | --- | --- |
| A0 | Python v1 | Aborted | None | None | Not launched |
| P1 | Python v1 | Control mismatch | `i had macaroni for dinner` | `i had pizza for dinner` | Not launched |
| P2 | Python v2 | Control mismatch | `i'm drinking water` | `i'm drinking juice` | Not launched |
| P3 | Python v3, mapped Del | Pipeline success | `my cat's name is mischa` | `my cats name is phoebe` | `RECEIVER_SAW: my cats name is phoebe` |
| N1 | Native Windows ConPTY | Pipeline success | `i hate architecture` | `i like architecture` | `CHILD_RECEIVED: i like architecture` |

The complete structured inventory, including byte lengths and hashes, is in
`data/trials.csv`. None of the four recovery candidates received a separate
post-disclosure operator confirmation; the operator exact-match field therefore
remains “not collected.”

### Native byte evidence

The native `N1` transcript is 528 bytes and has SHA-256
`43e910be54f032eb169a3dcb966a416a296911a6aab2401fdd07c897195d70f0`.
The 19-byte recovery candidate occurs literally at offsets 394–412. The edit
region at offsets 413–469 contains 18 repetitions of `08 20 08` and one
`0D 20 0D` sequence. The replacement begins at offset 470. Metadata recorded
19 physical Backspace presses, zero physical Del presses, and zero Home presses.
The child exited with code 0 after printing only the replacement.

The final erase differed because the input began at the left screen edge. After
the preceding erasures moved the cursor to the first column, Windows represented
the remaining visual erase as carriage return, space, carriage return. This is
a byte-level difference from the motivating macOS recording, whose prompt left
the draft to the right of the screen edge; it does not change the functional
result.

### Follow-up matrix results

All four matrix cases had status `success`, child exit code 0, and
`CHILD_RECEIVED: omega`; none contained `CHILD_RECEIVED: alpha`.

| Start column | Serialized Backspace | `08 20 08` | `0D 20 0D` | Child line |
| ---: | ---: | ---: | ---: | --- |
| 0 | `0x7f` | 4 | 1 | `omega` |
| 0 | `0x08` | 4 | 1 | `omega` |
| 4 | `0x7f` | 5 | 0 | `omega` |
| 4 | `0x08` | 5 | 0 | `omega` |

Within both starting-column pairs, replacing the ASCII self-label `0x7f` with
`0x08` made the two transcript byte streams identical. Thus, on this
configuration, starting column determined whether the fifth erase used the
left-edge form, while the two tested Backspace input bytes did not change the
erase output or the line delivered to the child. Exact hashes, byte lengths,
and edit-region hex are in `data/backspace-matrix.csv`.

![Figure 1. Method boundary and exact native byte evidence](figures/figure1-method-and-byte-evidence.svg)

**Figure 1.** The host records the ConPTY output stream while Windows processed
line mode edits the child's input. The lower panel reports the exact `N1` byte
layout. The diagram is explanatory; the `.typescript` file is the primary
evidence.

## Discussion

### Principal observation

The native trial answered the technical question for the declared path. A draft
that disappeared from the rendered input line remained recoverable from the
sequential ConPTY output stream, while the child application received the
committed replacement through `ReadConsoleW`. This is the same functional
separation described in the motivating macOS case: output recording and
application input are distinct layers (McCoy & Blu, 2026).

The result is not paradoxical. Echo makes the draft part of terminal output as
it is typed. Erasure then appends control effects; it does not retroactively
delete earlier bytes from a sequential file. Line input simultaneously permits
the console subsystem to withhold the editable buffer from the application
until Enter (Microsoft, 2021, 2023). On macOS, `script(1)` explicitly records
terminal output, including backspaces (Apple Inc., 2022). On Windows, the custom
host performed the analogous recording of ConPTY output.

The follow-up narrows the explanation of the nineteenth physical erase in
`N1`. Moving the draft away from column 0 removed the `0D 20 0D` edge form,
whereas changing the host's Backspace serialization from `0x7f` to `0x08` did
not change output in either column condition. The evidence therefore favors a
cursor-boundary explanation over an input-byte explanation for these runs.
The four cases are insufficient to define a portable erase grammar across
other Windows builds, terminal front ends, or operating systems.

### Simulation versus native evidence

The Python trials should not be merged with the native result. In `P1`–`P3`,
the recorder also implemented editing, so recoverability followed directly from
the harness design. `P3` additionally remapped physical Windows Del to backward
erase. Those trials were useful development evidence and are preserved, but
they do not establish native Windows line-editor behavior.

In `N1`, by contrast, the host forwarded keys and recorded output; Windows
processed mode maintained the line consumed by `ReadConsoleW`. The native
output itself contained the OS-generated erase representations. The scripted
`N0` control further established, before the physical trial, that the child
received only the post-edit line in this ConPTY configuration.

### Comparison with the reported 2015 Intel Mac attempt

The source repository states only that a later 2015 Intel Mac attempt lacked an
active `script` recorder and produced no recoverable `.typescript` artifact
(McCoy & Blu, 2026). Its history does not document why the recorder was absent.
That attempt is not a matched platform comparison: it contrasts an unrecorded
display with explicitly recorded macOS and Windows paths. No result here
attributes retention to processor architecture.

A controlled Intel Mac comparison would need to launch `/usr/bin/script` before
input, preserve the resulting transcript, record terminal modes and cursor
position, and inspect raw bytes. Apple documents `script` as an opt-in command,
not an always-on service (Apple Inc., 2022).

### Privacy and claim boundaries

The privacy-relevant finding is narrow: an explicitly enabled exact-stream
recorder can preserve composition history that the final display and submitted
line do not reveal. The recorders in this work were launched specifically for
the experiment. Process inspection after collection found no Python harness or
`ConPTYBackspace` recorder still running; the remaining PowerShell windows were
nonrecording shells kept open for visibility.

The evidence does not show that deleted drafts were independently retained by
keyboard hardware, an ordinary unrecorded Windows terminal, the Codex composer,
a local or cloud language model, Microsoft, Apple, OpenAI, or a network service.
It also does not show that every terminal recorder behaves identically. ConPTY
produces UTF-8 text interleaved with virtual-terminal sequences, and applications
can alter console modes or implement their own editor (Microsoft, 2022b, 2023).

### Limitations

This was an adaptive engineering session, not a preregistered experiment. The
same inspector helped design the instrumentation and later read the files.
There was one machine, one operator, one physical native trial, and no blinded
independent reviewer. The follow-up added four scripted cases but no additional
physical operators or platforms. The operator did not independently confirm
the recovery candidates after disclosure, so exact-match scoring is
unavailable. The phrases were ASCII; Unicode graphemes, input methods, wrapped
lines, cursor movement, and multiline editing were not tested. The
deterministic receiver established a line-delivery boundary but was not a
language model. Exact Python v1 and v2 source snapshots were not preserved.
Finally, the now-public transcripts contain local paths and deliberately
retained erased text; future additions require disclosure review.

## Conclusion

An explicitly recorded native Windows ConPTY session preserved a complete draft
that was visually erased with physical Backspace presses, while a child using
processed line input and `ReadConsoleW` received only the committed replacement.
In a scripted follow-up, starting column—but not the choice between `0x7f` and
`0x08` Backspace input—determined whether the last of five erasures used the
left-edge `0D 20 0D` representation on this system.
The result supports a recorder-mediated recovery mechanism analogous to the
documented macOS `script` case, with platform-specific redraw bytes. It does not
support broader claims about uninstrumented interfaces, model input, cloud
telemetry, or hardware architecture. Exact transcripts, hashes, metadata,
source code, and a verifier are retained in this public repository; independent
operator confirmation of the recovered strings was not collected.

## References

Apple Inc. (2022). *script(1): Make typescript of terminal session* [Manual
page]. Apple Open Source.
https://github.com/apple-oss-distributions/shell_cmds/blob/e256b9a97f9bbd751305b7af36cf751668fbb849/script/script.1

McCoy, T., & Blu. (2026). *Backspace Gate: A preregistered blinded test of exact
recovery from a deleted terminal draft* [Source code and research repository].
GitHub. https://github.com/tmccoy678/Backspace-Text-Retention

Microsoft. (n.d.). *Windows Terminal* [Computer software]. GitHub. Retrieved
October 27, 2026, from https://github.com/microsoft/terminal

Microsoft. (2021). *SetConsoleMode function*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/console/setconsolemode

Microsoft. (2022a). *CreatePseudoConsole function*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/console/createpseudoconsole

Microsoft. (2022b). *Pseudoconsoles*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/console/pseudoconsoles

Microsoft. (2022c). *Creating a pseudoconsole session*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/console/creating-a-pseudoconsole-session

Microsoft. (2023). *GetConsoleMode function*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/console/getconsolemode

Microsoft. (2025). *Windows Terminal sample code*. Microsoft Learn.
https://learn.microsoft.com/en-us/windows/terminal/samples

The Open Group. (2004). *General terminal interface*. In *The Open Group Base
Specifications Issue 6, IEEE Std 1003.1, 2004 edition*.
https://pubs.opengroup.org/onlinepubs/007904975/basedefs/xbd_chap11.html
