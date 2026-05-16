# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aaron K. Clark
"""Tests for the passphrase generator + CLI."""

from __future__ import annotations

import random

import pytest

from correcthorsebatterystaple import cli

WORDS = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"]


# A drop-in stand-in for secrets.SystemRandom that uses a seedable PRNG.
# NEVER ship this — it's predictable. Tests only.
class SeededRng:
    def __init__(self, seed: int) -> None:
        self._r = random.Random(seed)

    def choice(self, seq):
        return self._r.choice(seq)


# ---- generate ----


def test_generate_default_count_is_four():
    pp = cli.generate(WORDS, rng=SeededRng(0))
    assert pp.count("-") == 3  # 4 words → 3 separators


def test_generate_respects_num_words():
    pp = cli.generate(WORDS, num_words=6, rng=SeededRng(0))
    assert pp.count("-") == 5


def test_generate_respects_separator():
    pp = cli.generate(WORDS, separator="_", rng=SeededRng(0))
    assert "-" not in pp
    assert pp.count("_") == 3


def test_generate_capitalize_title_cases_each_word():
    pp = cli.generate(WORDS, capitalize=True, rng=SeededRng(0))
    for w in pp.split("-"):
        assert w[0].isupper()
        assert w[1:].islower()


def test_generate_picks_only_from_supplied_wordlist():
    pp = cli.generate(WORDS, num_words=10, rng=SeededRng(0))
    for w in pp.split("-"):
        assert w in WORDS


def test_generate_is_seed_reproducible_with_a_seeded_rng():
    # Sanity: two runs with the same seed produce the same output.
    a = cli.generate(WORDS, rng=SeededRng(42))
    b = cli.generate(WORDS, rng=SeededRng(42))
    assert a == b


def test_generate_different_seeds_likely_produce_different_output():
    # With an 8-word vocab + 4 picks there's a 1-in-4096 chance of collision;
    # different seeds will almost always differ.
    a = cli.generate(WORDS, rng=SeededRng(1))
    b = cli.generate(WORDS, rng=SeededRng(2))
    assert a != b


def test_generate_rejects_num_words_below_one():
    with pytest.raises(ValueError, match="num_words"):
        cli.generate(WORDS, num_words=0, rng=SeededRng(0))


def test_generate_rejects_empty_wordlist():
    with pytest.raises(ValueError, match="empty"):
        cli.generate([], rng=SeededRng(0))


# ---- entropy ----


def test_entropy_of_eff_long_list_matches_known_values():
    # 7776 words → 12.92 bits/word; 4 words → 51.70 bits.
    assert cli.entropy_bits(7776, 4) == pytest.approx(51.6996, abs=0.001)
    assert cli.entropy_bits(7776, 6) == pytest.approx(77.5494, abs=0.001)


def test_entropy_zero_for_degenerate_inputs():
    assert cli.entropy_bits(0, 4) == 0.0
    assert cli.entropy_bits(7776, 0) == 0.0


# ---- CLI ----


def test_cli_default_emits_one_line(capsys):
    rc = cli.main([])
    assert rc == 0
    out = capsys.readouterr().out.strip().split("\n")
    assert len(out) == 1
    # Default has 4 words → 3 hyphens.
    assert out[0].count("-") == 3


def test_cli_count_emits_multiple_lines(capsys):
    rc = cli.main(["--count", "5"])
    assert rc == 0
    out = capsys.readouterr().out.strip().split("\n")
    assert len(out) == 5


def test_cli_num_words_changes_word_count(capsys):
    rc = cli.main(["--num-words", "6"])
    assert rc == 0
    line = capsys.readouterr().out.strip()
    assert line.count("-") == 5


def test_cli_separator_applied(capsys):
    rc = cli.main(["--separator", "_"])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert "-" not in out
    assert out.count("_") == 3


def test_cli_show_entropy_emits_estimate_on_stderr(capsys):
    rc = cli.main(["--show-entropy"])
    assert rc == 0
    cap = capsys.readouterr()
    assert "estimated entropy" in cap.err


def test_cli_rejects_zero_num_words(capsys):
    rc = cli.main(["--num-words", "0"])
    assert rc == 2
    assert "num-words" in capsys.readouterr().err


def test_cli_rejects_zero_count(capsys):
    rc = cli.main(["--count", "0"])
    assert rc == 2
    assert "count" in capsys.readouterr().err


def test_cli_custom_wordlist(tmp_path, capsys):
    p = tmp_path / "tiny.txt"
    p.write_text("only\none\nword\n", encoding="utf-8")
    rc = cli.main(["--wordlist", str(p), "--num-words", "2"])
    assert rc == 0
    pp = capsys.readouterr().out.strip()
    for w in pp.split("-"):
        assert w in {"only", "one", "word"}


def test_cli_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0


def test_cli_capitalize(capsys):
    rc = cli.main(["--capitalize"])
    assert rc == 0
    pp = capsys.readouterr().out.strip()
    for w in pp.split("-"):
        assert w[0].isupper()
