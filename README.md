# HackRack Wordlist Generator
> HackRack Custom Module — Authorized use only.

```
  ────────────────────────────────────────────────────────────────

  ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ██╗███████╗████████╗
  ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██║██╔════╝╚══██╔══╝
  ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     ██║███████╗   ██║   
  ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██║╚════██║   ██║   
  ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║███████║   ██║   
   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚══════╝   ╚═╝   

  H A C K R A C K   W O R D L I S T   G E N E R A T O R
  HackRack Custom Module  |  Authorized use only.
  ────────────────────────────────────────────────────────────────
```

An interactive terminal wordlist generator with three powerful modes: custom smart wordlists, brute-force character combinatorics, and wordlist mutation.

---

## Installation

### Method 1 — Install as a system command (recommended on Kali Linux)

```bash
git clone https://github.com/youruser/hackrack-wordlist-generator
cd hackrack-wordlist-generator
sudo bash install.sh
```

After that, run from anywhere:

```bash
hackrack-wordlist
```

To uninstall:

```bash
pip3 uninstall hackrack-wordlist
```

### Method 2 — pip install manually

```bash
pip3 install -e .
hackrack-wordlist
```

### Method 3 — Run directly (no install)

```bash
python3 main.py
```

**Requirements:** Python 3.10+ · No third-party dependencies (stdlib only)

---

## Modes

---

### [1] Custom Wordlist

Builds a targeted wordlist from personal information about a specific target (name, date of birth, phone number, etc.).

#### Steps

| Step | What you enter | What it produces |
|------|---------------|-----------------|
| 1 | Names / words / usernames | Case + leet-speak variants |
| 2 | Dates in `mm/dd/yyyy` | 500+ format variants per date |
| 3 | Special characters (`@ ! $ …`) | Individual characters |
| 4 | Optional alphanumeric (phone, plate, house #) | Stripped + cased variants |
| 5 | Length range (`min-max`, e.g. `8-9`) | Used as a filter |
| 6 | *(automatic)* | Merges all tokens into `temp/main_cache.txt` |
| 7 | *(automatic)* | Combines tokens → `output/wordlist.txt` |

#### How it works

**Step 1 — String variants**

Every input word is expanded into all possible upper/lowercase combinations:

```
raheel → raheel, Raheel, RAHEEL, rAheel, rAHEEL, RAhEeL …  (2^n combos)
```

Then leet-speak substitutions are layered on top:

```
a → @       e → 3       i → !       o → 0       s → $ or 5
```

So `raheel` also becomes `r@heel`, `r@h33l`, `r@h33!`, `R@H33L` etc.

---

**Step 2 — Date variants**

Each date is exploded into hundreds of representations by combining:

- **Day forms:** `15`, `15th`
- **Month forms:** `10`, `oct`, `Oct`, `OCT`, `october`, `October`, `OCTOBER`
- **Year forms:** `1992`, `92`
- **Orderings:** `dd-mm-yy`, `mm-dd-yy`, `yy-mm-dd`, `yy-dd-mm`
- **Separators:** `/`, `-`, `.`, *(none)*
- **Standalone tokens:** `1992`, `92`, `15th`, `october` …

A single date like `10/11/1992` generates ~530 unique tokens.

---

**Step 3 — Special characters**

Characters can be entered one per line, space-separated (`@ ! #`), or together (`@!#`). Each is stored as a standalone token in the cache and later combined with strings/dates during generation.

---

**Step 4 — Optional alphanumeric**

For identifiers like phone numbers, vehicle plates, or house numbers:

```
0300-1234567  →  0300-1234567, 03001234567
ABC-123       →  ABC-123, abc-123, ABC123, abc123, 123, ABC, abc
42A           →  42A, 42a, 42, A, a
```

Separators (`-`, `_`, `.`, spaces) are stripped. Alpha and digit substrings are extracted as standalone tokens.

---

**Step 5-6 — Merge**

All cache files are merged with global deduplication (first-seen order preserved):

```
[+] temp/string_cache.txt   →     648 tokens
[+] temp/date_cache.txt     →   1,178 tokens
[+] temp/special_cache.txt  →       3 tokens
[+] temp/optional_cache.txt →       8 tokens
[*] Total unique tokens : 1,837
```

---

**Step 7 — Combination engine**

An iterative DFS (depth-first search) with early pruning generates every ordered multi-token combination within the length range:

- Max depth is **auto-computed** as `max_len ÷ shortest_token_length` — no combinations are missed
- A branch is **pruned immediately** when extending it cannot possibly stay within `max_len`
- Every candidate is deduplicated via a hash set before writing

```
token pool: ["raheel", "@", "1992"]  |  range: 8–9
→ "raheel@"     (depth 2)
→ "@raheel"     (depth 2)
→ "raheel1992"  (depth 2)
→ "1992@raheel" (depth 3)
→ "@raheel@"    (depth 3)
```

Live progress is printed every 10,000 words. Temp files are deleted automatically when done.

---

### [2] Brute-Force

Generates **every possible character-level combination** for a chosen charset across a length range. No intelligence — exhaustive coverage.

#### How it works

1. Pick a charset from the menu (or type a custom one):

   | # | Charset | Size |
   |---|---------|------|
   | 1 | Lowercase `a–z` | 26 |
   | 2 | Uppercase `A–Z` | 26 |
   | 3 | Digits `0–9` | 10 |
   | 4 | Special `!@#$…` | 32 |
   | 5 | Alphanumeric | 62 |
   | 6 | All printable | 94 |
   | 7 | Custom — type your own | — |

2. Enter a length range (`min-max`).

3. The tool shows the **exact combination count** before starting:
   ```
   Charset size : 10 chars
   Length range : 6 – 6
   Combinations : 1,000,000
   ```

4. `itertools.product(charset, repeat=length)` is iterated for each length from min to max, streaming every word directly to disk at ~3M words/sec.

Live progress shows percentage complete, words written, speed, and elapsed time.

Output → `output/bf_wordlist.txt`

---

### [3] Mutate Wordlist

Takes an **existing wordlist** and applies password-mutation rules to every word, generating a much larger mutated list.

#### How it works

1. **Load** any `.txt` wordlist (e.g. `rockyou.txt`, `output/wordlist.txt`).

2. **Choose mutations** (each is an independent Y/n toggle):

   | Mutation | Example |
   |----------|---------|
   | Case variations | `pass` → `Pass`, `PASS`, `pAsS`, `PaSs` … |
   | Leet substitutions | `pass` → `p@ss`, `p@$$`, `p455` … |
   | Common prefixes | `123pass`, `!pass`, `@pass` … |
   | Common suffixes | `pass123`, `pass!`, `pass2025` … |

3. **Custom prefixes/suffixes** — add your own on top of the built-in common list.

4. **Optional length filter** — discard mutations outside a length range.

For every expanded base form, the engine generates:
- The form itself
- Prefix + form
- Form + suffix
- Prefix + form + suffix *(all prefix × suffix combos)*

All output is globally deduplicated. Speed is typically 10K–25K mutated words/sec depending on mutation selection.

Output → `output/mutated_wordlist.txt`

---

## Output Files

| File | Mode | Description |
|------|------|-------------|
| `output/wordlist.txt` | 1 | Smart combined wordlist |
| `output/bf_wordlist.txt` | 2 | Brute-force wordlist |
| `output/mutated_wordlist.txt` | 3 | Mutated wordlist |

---

## Example Session (Mode 1)

```
❯ python main.py

  Select a mode:
  [1]  Custom wordlist
  ❯ 1

  string [1]: Raheel
  string [2]:                         ← empty line to finish

  date [1]: 10/11/1992
  date [2]:                           ← skip

  char [1]: @ !
  char [3]:                           ← skip

  value [1]: 0300-1234567
  value [2]:                          ← skip

  length range: 8-10

  [+] 1,837 unique tokens → temp/main_cache.txt
  [+] 315,025 words written to output/wordlist.txt
  [~] Temp cache cleared.
```

---

## Legal

This tool is intended for **authorized penetration testing**, CTF challenges, and security research only.  
Do **not** use against systems you do not own or have explicit written permission to test.
