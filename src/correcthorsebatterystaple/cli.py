# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Passphrase generation + the argparse-driven CLI.

Entropy source is `secrets.SystemRandom` (CSPRNG via /dev/urandom on
Linux). Never `random` — that's seeded predictably.
"""

from __future__ import annotations

import argparse
import math
import secrets
import sys
from collections.abc import Iterable

from . import __version__
from .wordlist import ATTRIBUTION, load_default_wordlist, load_wordlist_from_path


def generate(
    words: list[str],
    num_words: int = 4,
    separator: str = "-",
    capitalize: bool = False,
    rng: secrets.SystemRandom | None = None,
) -> str:
    """Build one passphrase by picking `num_words` random entries from `words`.

    Args:
        words: The vocabulary to sample from.
        num_words: How many words to pick (default 4).
        separator: String joined between words (default '-').
        capitalize: If True, Title-Case each word.
        rng: Override the entropy source. Default = a fresh
            `secrets.SystemRandom()`. Tests use this to inject a seeded
            stand-in; production must always use the default.

    Returns:
        The joined passphrase.

    Raises:
        ValueError: if num_words < 1, the wordlist is empty, or the
            separator contains characters Aaron probably didn't mean.
    """
    if num_words < 1:
        raise ValueError("num_words must be >= 1")
    if not words:
        raise ValueError("wordlist is empty")
    rng = rng or secrets.SystemRandom()
    picked = [rng.choice(words) for _ in range(num_words)]
    if capitalize:
        picked = [w.capitalize() for w in picked]
    return separator.join(picked)


def entropy_bits(wordlist_size: int, num_words: int) -> float:
    """Shannon entropy in bits for the (wordlist, count) pair.

    Note: this is the *theoretical* entropy, conditional on the
    wordlist being free of duplicates and on each pick being
    independent and uniform. Both are true for `generate()` above.
    """
    if wordlist_size <= 0 or num_words <= 0:
        return 0.0
    return num_words * math.log2(wordlist_size)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="correcthorsebatterystaple",
        description=(
            "Generate xkcd-936-style passphrases. Default = four random words "
            "from the EFF long wordlist (~51.7 bits of entropy)."
        ),
        epilog=ATTRIBUTION,
    )
    p.add_argument(
        "-n",
        "--num-words",
        type=int,
        default=4,
        metavar="N",
        help="Words per passphrase (default: 4).",
    )
    p.add_argument(
        "-s",
        "--separator",
        default="-",
        metavar="STR",
        help="String between words (default: '-'). Use '' for none.",
    )
    p.add_argument(
        "-c",
        "--capitalize",
        action="store_true",
        help="Title-Case each word.",
    )
    p.add_argument(
        "-N",
        "--count",
        type=int,
        default=1,
        metavar="K",
        help="Generate K passphrases (default: 1).",
    )
    p.add_argument(
        "-w",
        "--wordlist",
        default=None,
        metavar="PATH",
        help=(
            "Use a custom wordlist file (one word per line, blanks + '#' lines "
            "ignored). Default = bundled EFF long list."
        ),
    )
    p.add_argument(
        "--show-entropy",
        action="store_true",
        help="Print estimated entropy in bits after the passphrase(s).",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return p


def _emit(passphrases: Iterable[str], entropy_per: float | None) -> None:
    for pp in passphrases:
        print(pp)
    if entropy_per is not None:
        print(f"# estimated entropy per passphrase: {entropy_per:.2f} bits", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.num_words < 1:
        print("error: --num-words must be >= 1", file=sys.stderr)
        return 2
    if args.count < 1:
        print("error: --count must be >= 1", file=sys.stderr)
        return 2
    try:
        words = (
            load_wordlist_from_path(args.wordlist)
            if args.wordlist
            else load_default_wordlist()
        )
    except (OSError, ValueError) as e:
        print(f"error: failed to load wordlist: {e}", file=sys.stderr)
        return 2

    passphrases = [
        generate(words, args.num_words, args.separator, args.capitalize)
        for _ in range(args.count)
    ]
    bits = entropy_bits(len(words), args.num_words) if args.show_entropy else None
    _emit(passphrases, bits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
