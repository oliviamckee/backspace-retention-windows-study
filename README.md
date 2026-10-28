# Backspace retention on Windows: simulation and native ConPTY evidence

This public repository preserves a sequence of Windows experiments prompted by
the methods in McCoy and Blu's *Backspace Text Retention* repository. It contains
the exact locally generated terminal transcripts, their contemporaneous
metadata, the code used for the final simulation and native Windows trials, a
reproducible verifier, and a manuscript that separates observations from
interpretation.

> **Privacy notice:** this repository is public. The raw transcripts
> intentionally contain text that was typed and then visually deleted, as well
> as local paths. Review those fields before reusing the evidence or adding new
> transcripts.

## Evidence status

- The first launch was aborted before an experimental phrase was entered.
- Two Python-harness trials preserved erased drafts but failed their predeclared
  committed-control checks, so no receiver was launched.
- A third Python-harness trial completed the receiver boundary, but its physical
  Windows Del key was deliberately mapped to backward erase by the harness.
- The final trial used native Windows ConPTY line editing with physical
  Backspace input. The raw ConPTY stream retained the abandoned draft, while
  `ReadConsoleW` returned only the committed replacement line.
- A four-case scripted native follow-up crossed starting column 0 versus 4 with
  Backspace serialized as `0x7f` versus `0x08`. Starting column changed the
  final erase representation; the serialized byte did not change the output
  within either column pair.
- An October 28 ordinary PowerShell follow-up was not connected to a sequential
  recorder available to Aster during input. Olivia later supplied a plain-text
  screen copy and reported that Taylor had expected recovery of a phrase typed
  and erased before `phoebe is sleeping`. The copy contains the submitted
  `phoebe is sleeping` entry but no erased draft, Backspace byte, Delete byte,
  or terminal escape byte. No phrase could be recovered from that artifact.
- Public review of the Windows record prompted the matrix and a separate,
  instrumented replication on 2015 Intel Mac hardware. That later Mac
  replication used `/usr/bin/script -q` and published its exact artifacts in
  the source repository. It is not the earlier ordinary-shell attempt.
- Taylor stated publicly that the earlier Intel attempt occurred in an
  already-open ordinary Terminal shell and that `/usr/bin/script` was never
  launched. That statement is retained as retrospective operator testimony;
  no transcript or metadata from the earlier attempt was present in the public
  source repository at the October 28, 2026 capture cutoff.
- The operator did not provide a separate exact-match confirmation after any
  recovered draft was reported. The recovery strings are therefore direct
  byte-level candidates, not independently scored ground truth.

The full account, including limitations and APA references, is in
[MANUSCRIPT.md](MANUSCRIPT.md).

![Figure 1. Recorder and application boundary with native-trial byte evidence](figures/figure1-method-and-byte-evidence.svg)

## Follow-up Backspace matrix

The follow-up used the same native ConPTY/`ReadConsoleW` boundary and paced each
scripted key by 75 ms. Every case echoed and erased `alpha`, committed `omega`,
and ended with `CHILD_RECEIVED: omega`.

| Start column | Input byte | `08 20 08` | `0D 20 0D` |
| ---: | ---: | ---: | ---: |
| 0 | `0x7f` | 4 | 1 |
| 0 | `0x08` | 4 | 1 |
| 4 | `0x7f` | 5 | 0 |
| 4 | `0x08` | 5 | 0 |

After normalizing only the printed case label, the `0x7f` and `0x08`
transcripts were byte-identical within each starting-column pair. This supports
the left-edge explanation for `N1` on this configuration; it does not establish
a universal cross-platform erase grammar. Exact results are in
[`data/backspace-matrix.csv`](data/backspace-matrix.csv), with collection notes
in [`provenance/MATRIX_NOTES.md`](provenance/MATRIX_NOTES.md).

## Ordinary PowerShell screen-copy follow-up

This follow-up tested a different evidence path from the recorded ConPTY trial.
Aster could not see the open PowerShell window or its live input stream. After
the session, Olivia supplied
[`backspacetextretention2.txt`](evidence/screen-copies/backspacetextretention2.txt),
a 1,579-byte plain-text copy of the rendered PowerShell screen.

| Item | Directly preserved result |
| --- | --- |
| Olivia's operator report | Taylor gave real-time direction and expected recovery of a phrase Olivia typed and erased before `phoebe is sleeping`; Taylor was surprised when Aster did not recover it. |
| Visible submitted entry | `phoebe is sleeping`, followed by a PowerShell `CommandNotFoundException` for `phoebe` |
| Earlier erased phrase | Not present in the supplied file; no recovery candidate was produced |
| Editing bytes | Zero `0x08` Backspace, zero `0x7f` Delete, and zero `0x1b` escape bytes |
| Recorder marker | No PowerShell `Start-Transcript` header in the file |

The screen copy records the final rendered state, not the sequential editing
history. Its negative result therefore does not contradict the instrumented
ConPTY and `/usr/bin/script` trials: those paths created stream recorders before
input. The exact operator report, visible entries, byte counts, and claim
boundary are documented in
[`evidence/analysis/powershell-screen-copy-20261028.md`](evidence/analysis/powershell-screen-copy-20261028.md).
No new figure was added because this direct table is sufficient.

## Public review and Intel Mac context

The cross-platform follow-up contains two distinct Intel Mac events and one
Windows study. They are not interchangeable:

| Event | Recorder evidence | What the public record supports |
| --- | --- | --- |
| Earlier ordinary-shell attempt on a 2015 Intel Mac | No public transcript or metadata at the capture cutoff | Taylor later stated that the attempt occurred outside the wrapper and that `script` was never launched. This is operator testimony, not a contemporaneous process record. |
| Controlled replication on the same 2015 Intel Mac hardware, collected October 27, 2026 | Published `/usr/bin/script -q` transcript, terminal modes, launcher, receiver, hashes, and frozen recovery note | The recorder retained a 17-character candidate followed by 17 `08 20 08` erase triplets; the deterministic child reported only the committed line. Exact-match confirmation remained unscored. |
| This Windows ConPTY study | Exact local transcripts, metadata, source, hashes, and verifier in this repository | The explicitly enabled ConPTY-output recorder retained the abandoned draft while `ReadConsoleW` returned only the committed replacement. |

The Intel replication remains in its independently authored source repository
at immutable commit
[`eafc3a9`](https://github.com/tmccoy678/Backspace-Text-Retention/tree/eafc3a96f8b21a35acb89dd6619c806935720686/replications/intel-mac-2026-10-27).
The exact public comments that prompted the matrix, clarified the ordinary-shell
attempt, and defined the remaining evidence boundary are preserved in
[`evidence/public-comments/github-comments-20261028.md`](evidence/public-comments/github-comments-20261028.md).
No new figure was added for this update because the table distinguishes the
three records directly; Figure 1 remains limited to the Windows mechanism and
byte evidence.

## Repository layout

```text
data/                    Structured trial and follow-up-matrix indices
evidence/analysis/       Artifact-specific evidence and claim boundaries
evidence/matrix/         Exact follow-up ConPTY transcripts and metadata
evidence/public-comments/ Verbatim public-review and provenance transcripts
evidence/screen-copies/  Exact operator-supplied rendered-screen copies
evidence/transcripts/    Exact byte-preserved operator transcripts
evidence/metadata/       Exact contemporaneous JSON metadata
evidence/recovery-notes/ Contemporaneous notes preserved unchanged
evidence/self-tests/     Native ConPTY scripted control
figures/                 One explanatory SVG figure
provenance/              Source versions and evidentiary boundaries
src/python-simulation/   Final Python simulation harness
src/native-conpty/       Native Windows ConPTY host and child
tools/                   Read-only verification and rendering utilities
```

## Verify the evidence

From the repository root:

```powershell
python tools/verify_evidence.py
```

The verifier checks every evidence file against `SHA256SUMS` and asserts the
declared byte structures in the completed transcripts. To render control bytes
without altering a source transcript:

```powershell
python tools/render_transcript.py evidence/transcripts/conpty-experiment-20261027-223358.typescript
```

## Rebuild the native host

The native experiment requires Windows 10 version 1809 or later and .NET 9:

```powershell
dotnet build src/native-conpty/ConPTYBackspace.csproj -c Release
```

The host uses `CreatePseudoConsole` and records only the ConPTY output pipe. The
child enables processed, line, and echo input modes and reads the committed line
with `ReadConsoleW`.

Run the scripted 2×2 matrix from an attached Windows terminal:

```powershell
src/native-conpty/bin/Release/net9.0/ConPTYBackspace.exe --matrix --output-dir new-output
```

## Claim boundary

These files do not establish that an uninstrumented terminal, the Codex message
composer, a language model, OpenAI, Microsoft, Apple, or any network service
received deleted drafts. They show recoverability from explicitly enabled local
recorders on the declared paths.

## License

Original code and documentation in this repository are available under the MIT
License. Exact evidence artifacts remain factual records of the sessions in
which they were produced. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
for upstream attribution.
