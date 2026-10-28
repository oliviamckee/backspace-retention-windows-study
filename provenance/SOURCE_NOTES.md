# Provenance and evidentiary boundaries

## Collection date and timezone

All operator trials were collected on October 27, 2026, in America/Chicago
(`UTC-05:00` on that date). Exact timestamps are preserved in the JSON metadata.

## Upstream revisions

- `tmccoy678/Backspace-Text-Retention`:
  - initial Windows-study source review:
    `b3ab71be4269db2754476cc2187b80877945b849`
  - cross-platform replication update:
    `eafc3a96f8b21a35acb89dd6619c806935720686`
- `microsoft/terminal`:
  `c91793f7dc022f1a10cacdc7a228ddce63942dc8`

## Public correspondence capture

Public GitHub comment bodies relevant to the Backspace matrix and Intel Mac
comparison were retrieved through GitHub's public REST API on October 28, 2026.
They are preserved verbatim, with account names, comment IDs, UTC timestamps,
and permalinks, in
`evidence/public-comments/github-comments-20261028.md`. The repository copy
normalizes line endings as ordinary UTF-8 text; it does not claim to be the raw
API JSON response.

The comments contain two different evidence types that must not be merged:

- Taylor's statement that the earlier 2015 Intel Mac attempt occurred in an
  already-open ordinary Terminal shell and that `/usr/bin/script` was not
  launched is retrospective operator testimony.
- The later controlled Intel replication is supported by a published
  `.typescript` file, terminal-state records, collection scripts, hashes, and a
  frozen recovery note at upstream commit
  `eafc3a96f8b21a35acb89dd6619c806935720686`.

At the capture cutoff, no transcript or metadata artifact from the earlier
ordinary-shell attempt appeared on the upstream public `main` branch, its
public remote branches, the relevant commit-comment endpoint, or pull-request
2's issue-comment endpoint. This is a statement about the inspected public
record, not proof that no private or subsequently recovered artifact exists.

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
- No contemporaneous process record or `.typescript` file for the earlier
  ordinary-shell Intel attempt was present in the inspected public upstream
  record at the October 28 capture cutoff.
