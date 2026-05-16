# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Word source for passphrase generation.

By default loads the bundled EFF Long Wordlist (7776 words, ~12.92 bits
of entropy per word). The EFF list is the de facto diceware-grade
standard:

    https://www.eff.org/dice
    https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt

The bundled copy is CC BY 3.0 from the Electronic Frontier Foundation;
see ATTRIBUTION below and the NOTICE-style block at the bottom of the
README.

An operator can override with `--wordlist <path>` to use a custom file
(one word per line, ignoring blanks and `#` comments).
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

ATTRIBUTION = (
    "Default wordlist: EFF Long Wordlist by the Electronic Frontier "
    "Foundation, CC BY 3.0 (https://www.eff.org/dice)."
)

# The bundled wordlist filename inside the package.
_DEFAULT_WORDLIST = "eff_large_wordlist.txt"


def load_default_wordlist() -> list[str]:
    """Load the EFF long wordlist bundled with the package."""
    # `resources.files()` works whether the package is installed normally
    # or run from a source checkout.
    path = resources.files(__package__).joinpath(_DEFAULT_WORDLIST)
    text = path.read_text(encoding="utf-8")
    return _parse(text)


def load_wordlist_from_path(path: str | Path) -> list[str]:
    """Load a wordlist file from disk.

    Format: one word per line. Blank lines and `# ...` comment lines
    are ignored. Whitespace is stripped. Duplicates are NOT removed —
    if your wordlist has duplicates, the resulting passphrase
    entropy is overstated; clean the file first.
    """
    path = Path(path)
    return _parse(path.read_text(encoding="utf-8"))


def _parse(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    if not out:
        raise ValueError("Wordlist is empty — every line was blank or a comment.")
    return out
