# Backspace matrix provenance

## Reason for the follow-up

After public review, [a repository comment](https://github.com/oliviamckee/backspace-retention-windows-study/commit/1c2df2adc0e32b60260032fd6dcfa258aa24d1de#commitcomment-206991204)
proposed separating two possible influences on the native erase output: the
cursor's starting column and the byte used by the host to serialize Backspace.
The follow-up therefore crossed starting column 0 versus 4 with input byte
`0x7f` versus `0x08`.

## Final procedure

The updated native host ran four scripted ConPTY sessions on October 27, 2026.
In each case the child enabled processed, line, and echo input modes and called
`ReadConsoleW`. The host:

1. placed the editable input at column 0 or after a four-character `>>>>`
   prefix;
2. sent `alpha` one character at a time;
3. sent five Backspace bytes, either `0x7f` or `0x08`;
4. sent `omega` and carriage return; and
5. copied only the ConPTY output pipe to the exact `.typescript` file.

Each scripted key was separated by 75 ms so ConPTY emitted per-key erase output
rather than a coalesced whole-line redraw. All four children exited with code 0
and printed `CHILD_RECEIVED: omega`; none printed `CHILD_RECEIVED: alpha`.

## Final observations

| Start column | Serialized Backspace | `08 20 08` | `0D 20 0D` | Child line |
| ---: | ---: | ---: | ---: | --- |
| 0 | `0x7f` | 4 | 1 | `omega` |
| 0 | `0x08` | 4 | 1 | `omega` |
| 4 | `0x7f` | 5 | 0 | `omega` |
| 4 | `0x08` | 5 | 0 | `omega` |

Within each starting-column pair, the two transcript byte streams are identical
after replacing only the ASCII self-label `0x7f` with `0x08`. Thus, in these
four runs, starting column determined whether the last erase used the
left-edge `0D 20 0D` form; the two serialized Backspace bytes did not change
the erase output or committed line. This is a four-case observation on one
Windows/ConPTY configuration, not a general cross-platform grammar.

## Development observations

The first automated launch had no parent console and stopped before collection
while reading `Console.WindowWidth`; the host now uses fixed fallback dimensions
when that property is unavailable. A subsequent non-PTY launch reached the
child, but `GetConsoleMode(stdin)` failed before experimental input. Those four
status-failure artifacts were moved out of the publication tree and were not
treated as trials.

The first terminal-attached pilot sent scripted bytes without inter-key delays.
It completed, but ConPTY coalesced the rapid input into whole-line redraws. The
75 ms pacing was added before the final matrix was collected. The published
matrix contains the four paced runs only; their exact paths, hashes, and byte
counts are in `data/backspace-matrix.csv` and `SHA256SUMS`.
