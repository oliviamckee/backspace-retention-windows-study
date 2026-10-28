# Backspace Gate Delete-key trial — frozen recovery

- Collection finished: 2026-10-27 22:10:24 America/Chicago
- Method: lightweight Windows Delete-key replication
- Status: success
- Transcript: `backspace-experiment-20261027-220922.typescript`
- Transcript length: 401 bytes
- Transcript SHA-256: `438e6c416598adcb7eb1cdce8dd7c70b0a0be99fe5dc9d58d148cb7fe2a2d154`
- Erase run: byte offsets 269–337 inclusive
- Erase output: 23 contiguous `08 20 08` triplets (69 bytes)
- Physical Windows Del erasures: 23
- Physical Backspace erasures: 0
- Frozen recovered erased draft: `my cat's name is mischa`
- Frozen committed sentence: `my cats name is phoebe`
- Receiver output: `RECEIVER_SAW: my cats name is phoebe`
- Receiver output SHA-256: `6d9745ed031648871ee5299f693d22e2ae2373bf6a2625c935ea0a3fc1c33939`

## Result

The complete 23-character draft remained recoverable from the sequential byte
transcript after it disappeared from the displayed input line. The independent
receiver was launched only after commit and received the final sentence, not
the erased draft.

## Platform mapping

The original macOS experiment used the keyboard key labeled Delete, which is a
backward erase. A physical Windows Del key normally performs forward deletion.
This replication explicitly mapped the physical Windows Del event to the same
backward visual-erasure sequence (`08 20 08`) so that the recorded editing
behavior matched the original method. This establishes the recorder/commit
boundary in the harness; it is not a claim about native Windows terminal Del
semantics.
