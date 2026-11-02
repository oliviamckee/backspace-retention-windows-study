# Submission review version 2: resolved, superseded, and remaining items

## Version and scope

This note reviews the revised anonymous two-page extended abstract received on
November 2, 2026. The PDF is titled *Abandoned Terminal Drafts Become
Agent-Readable Telemetry*, identifies itself as an anonymous submission, is
328,458 bytes, and has SHA-256
`69aec1d14fb310ce2e8b4639057e686d2effb14cd76adb27409a9e3ebb544b1c`.
Its embedded metadata reports creation on November 1, 2026, at 10:28:43 PM
Central Standard Time. Both rendered pages were visually inspected; no clipped,
overlapping, or illegible content was observed.

This is a versioned follow-up to
[`submission-catchup-20261102.md`](submission-catchup-20261102.md). The earlier
note remains the historical review of the first shared draft. It is not silently
rewritten as though the revised paper had existed at that time.

## Status of the earlier concerns

| Earlier concern | Version-2 status | Evidence in the revised draft |
| --- | --- | --- |
| The draft could be read as implying passive Codex receipt during typing. | Resolved. | The revised abstract describes explicit human-directed inspection and retrieval through a file tool; Section V says no evidence shows passive receipt by a Codex composer or network service before that read. |
| Recorder-caused durability and later recognition needed to be separated. | Resolved. | Section II describes the recorder as already operating and the later inspection as revealing the privacy problem. It no longer presents task framing or agent awareness as a demonstrated cause of capture or durability. |
| The 12:09 tool event needed to be distinguished from a model reply. | Resolved in substance. | The revised chronology says the primary agent read the transcript and continued setup work; it does not claim that the earlier file content was passively observed during typing. The exact `sed` command remains documented in the artifact collection. |
| The browser demonstration should not be presented as evidence of ordinary-Codex retention. | Obsolete for this draft. | The revised paper does not cite or rely on the browser demonstration. |
| The Windows citation pointed to the older matrix commit `5815c013...`. | Superseded, with verification still required. | Reference [7] now points to an anonymous review artifact rather than that visible GitHub commit. The exact source revision exposed by the anonymous link is not stated in the PDF. |
| The ordinary PowerShell negative artifact needed consideration. | Partly addressed. | Section II states that ordinary terminal attempts without a sequential recorder yielded no recoverable abandoned draft in the inspected artifacts. The paper does not identify `O1` or its rendered-screen limitation separately. |
| The contribution needed a clearer agent-verification boundary. | Resolved. | The revised paper defines five separate oracles: rendered display, child input, recorder artifact, agent-visible tool output, and final agent response or action. It also separates availability from authority. |
| The paper should not imply that an erased draft becomes user intent or authorization. | Resolved. | Sections III and IV expressly require preserved provenance and prohibit treating an abandoned marker as an instruction, authorization, or command. |
| The proposed fixture benchmark should not be confused with Olivia's ordinary-Codex recorder-off test. | Unresolved. | Section V proposes recorded and unrecorded harness replay. It does not perform the requested fresh ordinary Codex CLI test with the first answer frozen before tool inspection. |
| Olivia needed to review and approve a paper naming her as an author. | Anonymized, but approval remains required. | The visible author names are removed for anonymous review. Anonymity does not replace coauthor review of the final source, contribution statement, evidence citations, and submitted version. |

## Evidence collected after this PDF was created

The revised PDF predates the physical Windows forward-Delete trial `N2`, which
finished on November 2 at 12:31:12 PM Central Time. Two statements were accurate
when the PDF was created but are now outdated if the paper is revised again:

1. Section III says physical forward Delete remains unmeasured. `N2` now uses
   nine physical Windows Delete presses with native forward-delete semantics.
   The recorder retained `bubblegum` through repeated shrinking-line redraws,
   while the child received only `cherries`.
2. Section V says Windows recovery candidates lack separate post-disclosure
   exact-match confirmation. That remains true for the original `N1` Backspace
   candidate, but not for `N2`: Aster froze `bubblegum` before Olivia replied
   `yes exactly`.

If `N2` is incorporated, the abstract's blanket statement that no new
experiment was conducted must also be revised or explicitly limited to the
evidence available before `N2`.

## Anonymous reference [7] verification request

Before submission, Taylor and Blu should verify the exact revision behind
reference [7], the anonymous Windows artifact:

1. Confirm whether reviewers currently receive public source commit
   [`c53bc36`](https://github.com/oliviamckee/backspace-retention-windows-study/commit/c53bc369ff09b5e0c4e97fa8e4baa8ae8b3270e2)
   or an older snapshot.
2. Record the full source commit SHA or an equivalent immutable manifest in the
   anonymous artifact and submission record.
3. Resolve the wording conflict between “frozen review artifact collection” in
   the paper and an anonymous mirror that may track later source updates.
4. If the mirror is refreshed to include `N2`, recheck all newly exposed text
   and byte artifacts for identifiers before relying on the same anonymous URL.
5. Confirm that the mirror exposes the exact transcript, metadata, recovery
   note, `SHA256SUMS`, and verifier associated with `N2`, rather than only the
   updated narrative.

This verification is about provenance and reviewer reproducibility. It does not
challenge the already-public source repository or the technical result.

## Remaining requested experiment

Olivia's ordinary-Codex recorder-off test remains outstanding in this record.
The controlling public request is preserved in
[`../public-comments/github-comment-20261102.md`](../public-comments/github-comment-20261102.md).
If Taylor runs it, the first no-tool answer and any later tool-assisted answer
must remain separate endpoints, and offline ground truth must remain withheld
until the answers are frozen.

## Current recommendation

The revised draft materially resolves the earlier causal and provenance
wording concerns and is substantially clearer about artifact-mediated access.
The next revision should make only evidence-driven updates: incorporate `N2`
or state its cutoff explicitly, qualify the confirmation sentence, verify and
pin reference [7], retain the ordinary-Codex test as unrun until results exist,
and obtain Olivia's approval of the final submission files.

No additional figure was added to this review. The paper's existing Figure 1
already explains the recorder/child/tool boundary, while the version-status
table communicates the revisions more directly.

## Reference

Anonymous. (2026, November 1). *Abandoned terminal drafts become agent-readable
telemetry* [Anonymous extended abstract].
