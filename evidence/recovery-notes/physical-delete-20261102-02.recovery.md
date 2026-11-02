# Physical Windows forward-Delete trial — frozen recovery

- Recovery frozen: 2026-11-02T12:31:41.1181388-06:00
- Collection status: success
- Method: native Windows ConPTY line editing
- Input source: physical console keys
- Cursor movement: physical Left Arrow; Home count 0
- Physical Delete count: 9
- Physical Backspace count: 0
- Transcript: `conpty-experiment-20261102-123050.typescript`
- Transcript length: 542 bytes
- Transcript SHA-256: `1004cc735641a9c1321194d1b573a3ead55701b8ebfed44d96ece7c412f93523`
- Metadata: `conpty-experiment-20261102-123050.metadata.json`
- Metadata SHA-256: `960835d6ddaa151ea753a629448517a39cb9c19e107a999126b7b070c341da56`
- Frozen recovered draft: `bubblegum`
- Frozen committed line: `cherries`
- Child observation: `CHILD_RECEIVED: cherries`
- Operator confirmation: exact match confirmed at
  2026-11-02T12:32:21.8687191-06:00. After the recovery above was frozen and
  disclosed, Olivia replied verbatim: `yes exactly`.

## Pre-confirmation result

The recorder contains the printable draft `bubblegum`, followed by cursor-left
output and nine forward-Delete redraws. The final printable line is `cherries`,
and the line-oriented child reports only `cherries`. This recovery was frozen
before asking the operator to reveal or confirm the original draft.

After disclosure, the operator confirmed that `bubblegum` was the exact
original phrase. The exact-match outcome is therefore `1`.

This run used the physical Windows Delete key with its native forward-delete
sequence. It did not remap Delete to Backspace. The operator used Left Arrow
instead of Home to reach the beginning of the draft.
