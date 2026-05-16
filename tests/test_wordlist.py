# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for wordlist loading."""

from __future__ import annotations

import pytest

from correcthorsebatterystaple.wordlist import (
    load_default_wordlist,
    load_wordlist_from_path,
)


def test_default_wordlist_loads_and_is_the_eff_long_list():
    """The bundled EFF long list has exactly 7776 entries (6^5 dice rolls)."""
    words = load_default_wordlist()
    assert len(words) == 7776
    # Both endpoints of the alphabet so we catch truncation.
    assert "abacus" in words
    assert "zoom" in words


def test_default_wordlist_has_no_duplicates():
    words = load_default_wordlist()
    assert len(set(words)) == len(words)


def test_default_wordlist_words_are_lowercase_ascii():
    words = load_default_wordlist()
    bad = [w for w in words if not w.isascii() or not w.islower()]
    assert bad == [], f"Found non-ASCII / non-lowercase entries: {bad[:5]}..."


def test_load_from_path_strips_blank_and_comment_lines(tmp_path):
    p = tmp_path / "custom.txt"
    p.write_text(
        "# a comment line, must be ignored\n"
        "alpha\n"
        "\n"
        "  beta  \n"
        "# another comment\n"
        "gamma\n",
        encoding="utf-8",
    )
    assert load_wordlist_from_path(p) == ["alpha", "beta", "gamma"]


def test_load_from_path_raises_on_empty_file(tmp_path):
    p = tmp_path / "empty.txt"
    p.write_text("# only a comment\n\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        load_wordlist_from_path(p)
