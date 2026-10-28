# Provenance and evidentiary boundaries

## Collection date and timezone

All operator trials were collected on October 27, 2026, in America/Chicago
(`UTC-05:00` on that date). Exact timestamps are preserved in the JSON metadata.

## Upstream revisions

- `tmccoy678/Backspace-Text-Retention`:
  `b3ab71be4269db2754476cc2187b80877945b849`
- `microsoft/terminal`:
  `c91793f7dc022f1a10cacdc7a228ddce63942dc8`

## Environment established by generated metadata

- Python simulation: Python 3.12.10 on `win32`.
- Native trial: Microsoft Windows 10.0.19045, x64, .NET 9.0.0.
- Native child exit code: 0.

## Source preservation

The `.typescript` files, JSON metadata, and contemporaneous recovery notes under
`evidence/` were copied without conversion. `SHA256SUMS` identifies those exact
copies. The recovery notes are preserved even where their wording predates the
later audit; the manuscript supersedes them for interpretation.

The current Python source is the final v3 harness. Exact v1 and v2 source
snapshots were not frozen during the session and are therefore not reconstructed
here. Their outputs and metadata remain exact. The native ConPTY source is the
source used for `N0` and `N1`.

## Uncollected evidence

- No independent operator record of the erased phrases was created.
- The operator did not answer the post-recovery exact-match questions.
- No packet capture, HID capture, Windows Event Tracing session, screen video,
  or cloud telemetry was collected.
- No claim is made about uninstrumented terminals or message composers.
