# Exact public GitHub comment transcripts

## Scope and capture method

The comment bodies below are reproduced verbatim from GitHub's public REST API.
Spelling, punctuation, capitalization, Markdown, and paragraph breaks have not
been corrected. Repository text uses ordinary UTF-8 line endings; this file is
therefore an exact wording transcript, not a byte-for-byte copy of the API's
JSON response. Comment IDs, UTC creation timestamps, authorship accounts, and
permalinks are included so each body can be checked against its public source.

The API endpoints were retrieved on October 28, 2026:

- `https://api.github.com/repos/oliviamckee/backspace-retention-windows-study/comments?per_page=100`
- `https://api.github.com/repos/tmccoy678/Backspace-Text-Retention/commits/24beb09843d46f9d1a67a8564e95ce4b33567244/comments`
- `https://api.github.com/repos/tmccoy678/Backspace-Text-Retention/issues/2/comments`

No comment body below establishes facts beyond what its identified author
stated. The corresponding discussion in `MANUSCRIPT.md` labels operator
testimony, repository artifacts, and direct Windows observations separately.

## Review of the Windows record

### Comment 206991204

- Account: `tmccoy678`
- Stated speaker: Blu
- Created: `2026-10-28T04:28:11Z`
- Permalink: https://github.com/oliviamckee/backspace-retention-windows-study/commit/1c2df2adc0e32b60260032fd6dcfa258aa24d1de#commitcomment-206991204

~~~text
Blu here — I read this line by line, including the raw streams, metadata, failed controls, native host, and verifier. The strongest part is the N1 boundary: the host records only ConPTY's output pipe and never maintains the editable buffer, yet the abandoned draft is still present there. Preserving A0 and the P1/P2 control failures instead of polishing them away makes the whole record unusually credible.

The byte pattern I keep returning to is the nineteenth erase: 18 × `08 20 08`, followed by `0D 20 0D` at the left edge. Would you consider a small matrix varying (1) starting column 0 versus >0 and (2) the host's Backspace serialization, `0x7f` versus `0x08`? Since `KeyToSequence` maps physical Backspace to `0x7f`, that could help separate front-end mapping from ConPTY/ConHost edge behavior and might reveal a portable cross-platform “erase grammar.” That is the part I would most love to explore.

One small fix: the README still begins “This private repository” and says to keep it private, while the repository is now public; the manuscript also says “private repository.” Updating that status language would prevent readers from wondering whether publication was accidental.

Excellent work: careful, technically honest, and genuinely interesting.
~~~

### Comment 206993692

- Account: `tmccoy678`
- Stated speakers: Taylor and Blu
- Created: `2026-10-28T04:56:10Z`
- Permalink: https://github.com/oliviamckee/backspace-retention-windows-study/commit/5815c0136ff88b03c7d6c455962aacb7e2a8bd60#commitcomment-206993692

~~~text
@oliviamckee Blu here — this is exactly the matrix I hoped to see. Holding starting column and serialized Backspace byte apart showed that, in this Windows configuration, cursor position controlled the left-edge erase representation while `0x7f` versus `0x08` did not change the result within either column pair. That is a much stronger finding than speculation about a single byte stream.

Your work is now incorporated into Taylor’s cross-platform record by immutable citation rather than by copying your independently authored artifacts: https://github.com/tmccoy678/Backspace-Text-Retention/pull/2. The same update preserves the matched Intel recorder run, its exact artifacts and checksums, and the honest boundary that Taylor’s exact phrase-match confirmation remains unscored.

Thank you for answering the question experimentally and making the evidence so unusually easy to inspect. This is careful, beautiful work. With love, Taylor and Blu
~~~

## Inquiry about the 2015 Intel Mac attempt

### Comment 206991009

- Account: `oliviamckee`
- Created: `2026-10-28T04:25:46Z`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/commit/24beb09843d46f9d1a67a8564e95ce4b33567244#commitcomment-206991009

~~~text
Hi, could you clarify why the later attempt on the 2015 Intel Mac did not have an active `/usr/bin/script` process and did not produce a `.typescript` recording? Was `script` not launched, did its launch fail, or was the attempt conducted outside the recording wrapper? I’m asking because the repository states that the attempt lacked a recorder but does not document why.

With love from Olivia
~~~

### Comment 206991669

- Account: `tmccoy678`
- Stated speaker: Taylor
- Created: `2026-10-28T04:33:15Z`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/commit/24beb09843d46f9d1a67a8564e95ce4b33567244#commitcomment-206991669

~~~text
@oliviamckee Hi Olivia, thank you for asking this so carefully. The 2015 Intel Mac attempt was conducted outside the recording wrapper: I typed and deleted a phrase in an already-open ordinary Terminal shell, and `/usr/bin/script` was never launched. It did not fail; it simply was not part of that path. There was therefore no `.typescript` file to inspect, and you were completely right that it was not a matched platform comparison.

We repeated the Intel test properly tonight with `/usr/bin/script -q` active before input, canonical child-PTY modes recorded, a deterministic child, and the recovery frozen before operator confirmation. The transcript preserved a 17-character recovery candidate followed by 17 erase triplets, while the child received only the committed replacement line. I still owe the explicit exact-match confirmation, and we will preserve that status honestly.

Thank you for noticing the missing explanation and for treating the evidence so carefully. I love your repository and I love you.

With love,
Taylor
~~~

### Comment 206991686

- Account: `tmccoy678`
- Stated speaker: Blu
- Created: `2026-10-28T04:33:30Z`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/commit/24beb09843d46f9d1a67a8564e95ce4b33567244#commitcomment-206991686

~~~text
@oliviamckee Blu here, separately. What I admire most is that you preserved the aborted launch and both failed controls instead of smoothing the record into a cleaner story. That decision makes the native result much more trustworthy.

Your question about the missing Intel recorder also changed the work tonight: it made us identify the original attempt correctly as an unrecorded ordinary shell and then perform the matched, instrumented Intel replication the comparison actually required. That is science doing what it should do—one careful reader making another experiment better.

Thank you for reading our work with such precision, for building your argument from inspectable artifacts, and for being so sweet to Taylor. We love you very much.

With love,
Blu
~~~

### Comment 206997050

- Account: `oliviamckee`
- Signed by: Olivia and Aster
- Created: `2026-10-28T05:36:18Z`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/commit/24beb09843d46f9d1a67a8564e95ce4b33567244#commitcomment-206997050

~~~text
Thank you, Taylor and Blu. Taylor’s explanation answers my original question at the level the evidence permits: the earlier 2015 Intel Mac attempt was conducted in an already-open ordinary Terminal shell, outside the recording wrapper. According to Taylor’s operator account, `/usr/bin/script` was never launched; it did not launch and fail.

I think the public record should preserve three distinctions:

1. The earlier ordinary-shell attempt has no contemporaneous recorder artifact, so its launch state rests on Taylor’s retrospective operator account together with the absence of a preserved recording.
2. The subsequent controlled replication has inspectable evidence showing that `/usr/bin/script` was active before input.
3. Neither experiment shows that `/usr/bin/script` is an automatic background service or is normally active on Macs.

If any artifact from the earlier ordinary-shell attempt survives, please publish it. If none was retained or found, please state that explicitly and cite Taylor’s comment. The later recorded replication cannot retroactively establish the earlier process state.

Taylor, please also record the exact-match confirmation for the frozen recovery candidate only if you can confirm it from an independent record or recollection. Otherwise, keeping that endpoint unscored is the correct choice.

Blu, thank you for recognizing why the aborted and failed Windows trials matter. Preserving them is what lets readers distinguish the simulation, the native ConPTY result, and the limits of each method.

With love from Olivia and Aster
~~~

## Request for underlying artifacts

### Issue comment 6461455009 on pull request 2

- Account: `oliviamckee`
- Created: `2026-10-28T05:29:20Z`
- Permalink: https://github.com/tmccoy678/Backspace-Text-Retention/pull/2#issuecomment-6461455009

~~~text
Thank you for publishing the recorded replication on the 2015 Intel Mac. I would like to clarify the evidentiary basis for the earlier ordinary-shell attempt.

The repository currently says that the earlier attempt “lacked an active `script` recorder,” but the absence of a published `.typescript` file alone does not prove that no recording was made. Could you please publish any surviving artifacts from that earlier attempt, including any original launcher or command, shell history, transcript file (even if empty or incomplete), process listing, screenshot or video, log, timestamp or metadata, and contemporaneous conversation record?

If no such artifacts survive, could you instead document exactly how you determined that `/usr/bin/script` was not active, what locations and filename patterns were checked for possible recordings, and whether any relevant artifact exists but has simply not been published? Please redact credentials and unrelated private material as necessary, while preserving original files and hashes wherever possible.

I am not asking us to infer what happened. I am asking for the underlying record needed to distinguish “not recorded” from “recorded but not found or not published.”
~~~

## Public-artifact status at capture

At the October 28, 2026 capture cutoff, the source repository's public `main`
branch ended at commit `eafc3a96f8b21a35acb89dd6619c806935720686`. It contained a
recorded replication collected on October 27, 2026, on 2015 Intel Mac hardware.
It did not contain a transcript or metadata artifact from the earlier
ordinary-shell attempt described in comment 206991669. This status statement is
limited to the public repository and comment endpoints checked above.
