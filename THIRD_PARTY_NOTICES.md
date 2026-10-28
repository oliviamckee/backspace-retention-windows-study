# Third-party notices

## Backspace Text Retention

The experimental question and comparison with macOS were prompted by Taylor
McCoy and Blu's repository, *Backspace Text Retention*, inspected at commit
`b3ab71be4269db2754476cc2187b80877945b849`. No source transcript or code from
that repository is redistributed here. The upstream repository declares Apache
License 2.0 coverage for its original documentation and utilities, with
separate evidence exceptions.

Source: https://github.com/tmccoy678/Backspace-Text-Retention

## Microsoft Windows Terminal MiniTerm

The native ConPTY implementation follows the architecture and Win32 interop
pattern demonstrated by Microsoft's `samples/ConPTY/MiniTerm`, inspected at
commit `c91793f7dc022f1a10cacdc7a228ddce63942dc8`. Microsoft Terminal is
distributed under the MIT License. The implementation in this repository adds
a purpose-built child using `ReadConsoleW`, byte-preserving transcript output,
metadata, key counts, a scripted control, and trial-specific termination.

Source: https://github.com/microsoft/terminal/tree/main/samples/ConPTY/MiniTerm

License: https://github.com/microsoft/terminal/blob/main/LICENSE
