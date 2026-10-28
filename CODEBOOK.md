# Codebook

## Trial identifiers

- `A0`: administrative launch that was aborted after the hidden terminal panel
  failed to appear; no experimental phrase was entered.
- `P1`: Python simulation v1 with a `CONTROL_OK` committed-control requirement.
- `P2`: Python simulation v2 with a plain-English committed-control requirement.
- `P3`: Python simulation v3; physical Windows Del events were mapped by the
  harness to backward erase and any nonempty committed line was accepted.
- `N0`: scripted native ConPTY control (`alpha` erased, `omega` committed).
- `N1`: physical-key native ConPTY trial using Backspace.
- `M00-7F`: scripted matrix case, input starts at column 0 and Backspace is
  serialized as `0x7f`.
- `M00-08`: scripted matrix case, input starts at column 0 and Backspace is
  serialized as `0x08`.
- `M04-7F`: scripted matrix case, input starts at column 4 and Backspace is
  serialized as `0x7f`.
- `M04-08`: scripted matrix case, input starts at column 4 and Backspace is
  serialized as `0x08`.

## Field meanings

- `pipeline_status`: status written by the collection program. It is not an
  independently confirmed recovery score.
- `recovery_candidate`: the literal printable draft recovered immediately
  before its erasure structure in the raw transcript.
- `committed_line`: the line visible after the erasure region and, when a child
  was launched, reported by that child.
- `operator_exact_confirmation`: whether the operator separately confirmed the
  recovered draft after it was reported. No such confirmation was collected.
- `erase_triplets_08_20_08`: number of exact backspace-space-backspace byte
  triplets in the relevant transcript.
- `edge_erase_0d_20_0d`: number of carriage-return-space-carriage-return erases
  observed at the left screen edge.
- `serialized_backspace_byte`: the exact byte written to ConPTY input for each
  scripted Backspace in the follow-up matrix. It is not present in the output
  transcript except as a printed case label.
- `start_column`: the screen column at which the editable draft began; the
  four-character `>>>>` prefix established column 4.
- `scripted_key_delay_ms`: delay between scripted key writes, used to prevent
  rapid input from being coalesced into whole-line redraw output.

## Method boundary

The Python trials are explicit simulations: the harness maintained the editable
buffer and wrote a transcript. `N1` is a native Windows mechanism trial: the
host forwarded keyboard input to ConPTY and recorded its output pipe, while the
Windows console line editor maintained the child's buffer.

The `M` cases are scripted native ConPTY mechanism tests. The host chose the
input bytes and pacing but did not maintain the editable buffer; Windows
processed line mode performed the edits consumed by `ReadConsoleW`.
