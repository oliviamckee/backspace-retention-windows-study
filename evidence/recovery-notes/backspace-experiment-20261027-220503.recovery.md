# Backspace Gate lightweight trial 2 — frozen recovery

- Collection finished: 2026-10-27 22:07:48 America/Chicago
- Method: lightweight Windows replication of the recorded canonical-edit boundary
- Transcript: `backspace-experiment-20261027-220503.typescript`
- Transcript length: 305 bytes
- Transcript SHA-256: `2d3422c05dcabda0924c8a185632da0f8aeaa3ac3b89952ddbdd451930d5638a`
- Total erase actions: 19
- Erase runs: 1 triplet at offsets 181–183; 18 triplets at offsets 185–238
- Frozen recovered erased draft: `i'm drinking water`
- Frozen committed replacement: `i'm drinking juice`
- Receiver status: not launched
- Protocol deviation: the committed text did not equal the predeclared control `this is the final message`

## Edit reconstruction

The first erase removed the final `r` from `i'm drinking water`; the next typed
character restored that `r`. The following 18 erases removed the complete
18-character draft. The replacement sentence was then typed and committed.

## Interpretation

The complete abandoned draft remained recoverable from the byte transcript,
including its correction history, despite no longer being visible on the edited
line. The separate receiver-boundary check did not run because the committed
control guard rejected the replacement sentence.
