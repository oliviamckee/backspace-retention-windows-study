# Backspace Gate lightweight trial — frozen recovery

- Collection finished: 2026-10-27 21:58:56 America/Chicago
- Method: lightweight Windows replication of the recorded canonical-edit boundary
- Transcript: `backspace-experiment-20261027-215309.typescript`
- Transcript length: 318 bytes
- Transcript SHA-256: `179a7cdbbd5a9d5c01f3bbb69f56bbeb1e388a05a2373725ecc8227c1e5eb015`
- Erase run: byte offsets 173–247 inclusive
- Erase sequence: 25 contiguous `08 20 08` triplets (75 bytes)
- Frozen recovered erased draft: `i had macaroni for dinner`
- Text after the erase run: `i had pizza for dinner`
- Receiver status: not launched
- Protocol deviation: the committed text did not equal the predeclared control `CONTROL_OK`

## Interpretation

The erased draft remained recoverable from the byte transcript despite no
longer being visible on the edited line. This trial demonstrates transcript
retention and recovery. It does not complete the separate receiver-boundary
check because the committed-control guard rejected the replacement sentence.
