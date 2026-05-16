# correcthorsebatterystaple

> "Through 20 years of effort, we've successfully trained everyone to use passwords
> that are hard for humans to remember, but easy for computers to guess."
> — [xkcd 936](https://xkcd.com/936/)

An xkcd-936-style passphrase generator. Four random common words from the
EFF Long Wordlist (~51.7 bits of entropy), generated with `secrets.SystemRandom`.
Stdlib only.

[![Tests](https://github.com/CryptoJones/correcthorsebatterystaple/actions/workflows/test.yml/badge.svg)](https://github.com/CryptoJones/correcthorsebatterystaple/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache)](LICENSE)
[![Codeberg](https://img.shields.io/badge/Codeberg-CryptoJones%2Fcorrecthorsebatterystaple-2185D0?logo=codeberg&logoColor=white)](https://codeberg.org/CryptoJones/correcthorsebatterystaple)
[![GitHub](https://img.shields.io/badge/GitHub-CryptoJones%2Fcorrecthorsebatterystaple-181717?logo=github&logoColor=white)](https://github.com/CryptoJones/correcthorsebatterystaple)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![xkcd 936](https://img.shields.io/badge/xkcd-936-blue)](https://xkcd.com/936/)
[![Version](https://img.shields.io/badge/version-v0.1.0-orange)]()

> Mirrored on both [GitHub](https://github.com/CryptoJones/correcthorsebatterystaple) and
> [Codeberg](https://codeberg.org/CryptoJones/correcthorsebatterystaple). Issues filed on
> either are welcome; commits are pushed to both.

---

## What it does

Generates passphrases like `correct-horse-battery-staple` — four (or N)
random common words joined by a separator. The entropy comes from
`secrets.SystemRandom` (CSPRNG via `/dev/urandom`), and the word source
is the [EFF Long Wordlist](https://www.eff.org/dice) — 7776 hand-curated,
unambiguous English words, ~12.92 bits of entropy each.

| N words | Entropy (bits) | Roughly comparable to |
|---|---|---|
| 4 | 51.7 | 9-char fully-random alphanumeric |
| 5 | 64.6 | 11-char fully-random alphanumeric |
| 6 | 77.5 | 13-char fully-random alphanumeric |
| 7 | 90.4 | 16-char fully-random alphanumeric |

(6 words is the modern "this should survive a determined offline attack
through 2030+" recommendation.)

## Install

```bash
pip install correcthorsebatterystaple
```

Or from source:

```bash
git clone https://github.com/CryptoJones/correcthorsebatterystaple.git
cd correcthorsebatterystaple
pip install -e .
```

Two entry points are installed: `correcthorsebatterystaple` (the full name)
and `chbs` (the convenient short alias).

## Quick start

```bash
$ chbs
arrest-acrobat-gloom-zit

$ chbs --num-words 6
phonics-saturated-twirl-undertow-aviation-pretzel

$ chbs --num-words 6 --separator ' '
shipping eggshell unmuted radial maker dabbing

$ chbs --capitalize
Cosmetics-Decimal-Pancake-Wildcat

$ chbs --count 5
unpacking-stoning-cosponsor-deafness
hardly-dilation-deviator-extrude
attest-cling-unbutton-quiver
gathering-mistrust-mortified-overstuff
diction-dwelling-cutlery-tremble

$ chbs --show-entropy
silvery-shameless-eyedrops-cyclic
# estimated entropy per passphrase: 51.70 bits

$ chbs --num-words 6 --show-entropy
crystal-banking-shawl-radial-anymore-curfew
# estimated entropy per passphrase: 77.55 bits

$ chbs --wordlist /usr/share/dict/words --num-words 4
```

## CLI reference

```
correcthorsebatterystaple [-h] [-n N] [-s STR] [-c] [-N K] [-w PATH] [--show-entropy] [--version]
```

| Flag | Default | Description |
|---|---|---|
| `-n N` / `--num-words N` | 4 | Words per passphrase |
| `-s STR` / `--separator STR` | `-` | String between words (use `''` for none) |
| `-c` / `--capitalize` | off | Title-Case each word |
| `-N K` / `--count K` | 1 | Generate K passphrases |
| `-w PATH` / `--wordlist PATH` | bundled EFF long list | Custom wordlist (one word per line, `#` comments ignored) |
| `--show-entropy` | off | Print estimated entropy on stderr after output |
| `--version` |  | Print version + exit |

## Why not just `pwgen` / `apg` / `openssl rand`?

Those generate random *strings*. The xkcd-936 insight is that random *words*
are easier for humans to remember at equivalent entropy, and easier to type
correctly under stress (no `l`/`1` / `O`/`0` confusion).

Use this when the passphrase needs to be:
- Memorable (master password, GPG key, disk-encryption passphrase)
- Recoverable from a phone-photo of a sticky note
- Speakable over the phone to your future self

Use `openssl rand -hex 32` when the passphrase only ever needs to be
machine-stored (API token, K8s secret).

## Wordlist attribution

The bundled wordlist is the [EFF Long Wordlist](https://www.eff.org/dice)
by the Electronic Frontier Foundation, licensed CC BY 3.0.

Source file: [eff_large_wordlist.txt](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt).

The original file has each line in `<dice-roll>\t<word>` format; this
project strips the dice-roll prefix on import. The dice-roll column is
preserved upstream for operators who want to generate passphrases by
literally rolling five physical dice per word (the most paranoid /
air-gapped path).

To redistribute or fork: the EFF wordlist must be re-attributed under
CC BY 3.0; the rest of this project is Apache 2.0.

## License

Apache 2.0 for the code. EFF Long Wordlist is CC BY 3.0 (see Wordlist
attribution above). See [LICENSE](LICENSE) for the Apache 2.0 text.

Proudly Made in Nebraska. Go Big Red! 🌽 https://xkcd.com/2347/
