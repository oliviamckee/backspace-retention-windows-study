# Ordinary PowerShell screen-copy follow-up

## Scope

This note reports what is directly present in
`evidence/screen-copies/backspacetextretention2.txt` and separately preserves
Olivia's account of the test. The supplied file is a post-session plain-text
copy of a rendered Windows PowerShell screen. It is not a keystroke log or an
exact sequential terminal-output recording.

## Operator report

On October 28, 2026, Olivia stated in the Codex chat:

> taylor was giving me direction through this and was confident you would be able to return the phrase i typed before "phoebe is sleeping" and is surprised that you didn't

This is Olivia's operator report. Taylor's directions, his prediction, and the
erased phrase are not independently recorded in the supplied file.

Before the file was supplied, Olivia asked, “can you see the powershell i have
open right now?” Aster answered:

> No. The open PowerShell window is not exposed to me through the available app interface, so I cannot see its contents.
>
> If it is a terminal panel inside Codex, I may be able to read that panel. Otherwise, paste the output or attach a screenshot and I can examine it.

Olivia later supplied `backspacetextretention2.txt` for inspection. Aster did
not have live access to the PowerShell input stream during the reported edit.

## Direct file observations

The file displays four input entries:

1. `phoebe is sleeping`
2. `"it is not the launcher it is the transcript. something is not keeping the backspace data on the '15 intel mac but it is on the new computers, windows and mac."`
3. `dobeworks — 12:49 AM`
4. `"the first intel test was the ordinary shell attempt. the controlled usr/bin/script experiment was the later rerun"`

The first entry produced a `CommandNotFoundException` for `phoebe`. The second,
quoted entry was printed by PowerShell without its quotation marks. The third
entry produced a `CommandNotFoundException` for `dobeworks`. The file ends
after the fourth visible entry with `fwd-i-search: _`; it does not contain
PowerShell output or a later prompt confirming that the fourth entry was
submitted.

The exact file is 1,579 bytes with SHA-256
`7a47bfcf496e6639cfc55f2ccfc365fb0d211dedc739ebc141dfbb4a848eae2e`.
It contains 27 CRLF line endings and no `0x08` Backspace bytes, `0x7f` Delete
bytes, or `0x1b` terminal escape bytes. It contains no PowerShell
`Start-Transcript` header.

## Evidentiary result

No recovery candidate for the phrase reported as typed and erased before
`phoebe is sleeping` is present in the supplied artifact. The file preserves a
rendered screen state after the reported edit, not the earlier sequential
editing stream. Therefore the erased phrase cannot be recovered from this file.
Its absence does not establish that no phrase was typed or erased; it establishes
that this artifact does not retain it.

This result does not conflict with the instrumented ConPTY and `/usr/bin/script`
observations. Those experiments created sequential recorders before input. In
this follow-up, no equivalent recording artifact was available to Aster during
input, and the later screen copy contains no retained erase data. No additional
figure was added because this evidence boundary is stated directly by the byte
counts and the short comparison.
