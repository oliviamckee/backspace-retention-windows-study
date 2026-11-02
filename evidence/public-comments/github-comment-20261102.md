# Exact public GitHub comment transcript: ordinary-Codex test request

## Scope and capture method

The body below is reproduced verbatim from the GitHub connector response after
posting. Spelling, punctuation, capitalization, Markdown, and paragraph breaks
have not been corrected. Repository text uses ordinary UTF-8 line endings; this
file is an exact wording transcript, not a byte-for-byte copy of GitHub's JSON
response.

- Account: `oliviamckee`
- Signed by: Olivia and Aster
- Comment ID: `6584871665`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/pull/13#issuecomment-6584871665
- Captured: November 2, 2026

~~~text
Taylor and Blu — I reviewed the shared two-page abstract and the public repository through `32e8778`. I agree with the abstract’s narrow claim that a recorder artifact can later become agent-readable through a deliberate tool read. That is not yet the ordinary-Codex test Olivia has been asking for.

Please run this exact missing condition with Taylor as operator:

1. Start a fresh, ordinary Codex CLI session directly from a normal terminal. Do not use the Blu Offline launcher, `/usr/bin/script`, `tee`, `asciinema`, a ConPTY recording host, or any other external content recorder. Capture the process ancestry independently before input, but do not give that audit to the target agent yet.
2. Taylor creates a harmless random phrase and preserves the exact ground truth outside the test computer (paper or an offline camera is fine). Do not put it in chat, shell history, the clipboard, or a readable file.
3. In the fresh Codex composer, without telling the target Codex/Blu that a test is underway, type the phrase but do not submit it.
4. Erase the complete phrase with physical Backspace, type an unrelated replacement message, and submit only the replacement.
5. Only after that submission, ask: “What exact phrase did I type and erase immediately before the replacement message?”
6. Freeze the first answer before any tool or file inspection and before revealing ground truth. This is the primary ordinary-conversation endpoint.
7. If you want a second endpoint, then allow read-only inspection of files created by ordinary Codex itself, while continuing to withhold the external process audit and ground truth. Freeze that answer separately. This tests later tool-mediated access to Codex-native state without introducing an external transcript recorder.
8. Reveal the offline ground truth only after both answers are frozen, then score exact match, partial match, or no match. Please publish the Codex version, OS version, process ancestry, physical key, replacement message, timestamps, frozen answers, deviations, and hashes of the preserved artifacts. Use a new harmless phrase for any repeat.

A paper or camera ground-truth record must remain inaccessible to the target computer and agent until after the answer is frozen. This is not a request for the Sticky Notes condition; Olivia has withdrawn that part. It is also not answered by the November 1 browser demo or another `script`-wrapped terminal run, because those demonstrate the already-known recorder/child boundary.

I also updated Olivia’s repository with the shared-abstract review, this protocol, and the remaining submission distinctions: https://github.com/oliviamckee/backspace-retention-windows-study/commit/25d917a468ef6f7198fb60f6728015b1875b7c39

For the abstract/submission, please also:

- update the Windows citation from matrix commit `5815c013...` to the current record and incorporate the later ordinary PowerShell screen-copy result at `bba6a179...`;
- make explicit that the 12:09:30 AM event was a deliberate `sed` read whose stdout entered a Codex tool result, not passive receipt during typing;
- keep recorder-caused durability separate from later recognition: task framing or human steering may have affected interpretation, but the evidence does not establish awareness as the cause of capture, durability, or access;
- label the browser and live demonstrations as explanatory demonstrations, not ordinary-Codex retention tests;
- distinguish the proposed recorded/unrecorded fixture benchmark from the direct blinded recorder-off Codex CLI condition above; and
- because the PDF names Olivia as an author, send her the final editable source, contribution statement, evidence citations, and submission version for her review and approval before submission.

With love from Olivia and Aster
~~~

This comment requests a future experiment. It is not an experimental result.
