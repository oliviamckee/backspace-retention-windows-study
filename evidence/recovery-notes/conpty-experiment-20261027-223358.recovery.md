# Native Windows ConPTY Backspace trial — frozen recovery

- Collection finished: 2026-10-27 22:35:49 America/Chicago
- Method: native Windows ConPTY with `ReadConsoleW` processed line input
- Status: success
- Operating system: Microsoft Windows 10.0.19045, x64
- Transcript: `conpty-experiment-20261027-223358.typescript`
- Transcript length: 528 bytes
- Transcript SHA-256: `43e910be54f032eb169a3dcb966a416a296911a6aab2401fdd07c897195d70f0`
- Physical Backspace presses: 19
- Physical Home presses: 0
- Physical Del presses: 0
- Frozen recovered erased draft: `i hate architecture`
- Frozen committed sentence: `i like architecture`
- Child output: `CHILD_RECEIVED: i like architecture`
- Child exit code: 0

## Byte evidence

The 19-byte erased draft occurs literally at transcript offsets 394–412. The
following edit region at offsets 413–469 contains 18 `08 20 08` erase triplets
and one final line-start erase encoded as `0D 20 0D`. The committed replacement
begins at offset 470.

## Result

The native Windows console line editor, running inside ConPTY with processed,
line, and echo input modes enabled, retained the complete abandoned draft in
the sequential ConPTY output stream. `ReadConsoleW` returned only after Enter
and supplied the committed replacement line to the child process.

The host forwarded keyboard input and recorded the ConPTY output bytes. It did
not maintain or edit the child's line buffer. This is therefore a native
Windows pseudoconsole/console-mode result, unlike the earlier Python simulation.
