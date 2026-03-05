#!/usr/bin/env python3
"""
Wordlist Generator — built step by step.
Step 4: After collecting strings, generate all case variations
        and write them to temp/string_cache.txt.
"""

import itertools
import os
import sys

# ─────────────────────────────────────────────────────────────
#  Colour helpers
# ─────────────────────────────────────────────────────────────

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def c(text: str, *codes: str) -> str:
    if not sys.stderr.isatty():
        return text
    return "".join(codes) + text + RESET


def prompt(label: str) -> str:
    sys.stderr.write(c(f"  {label}", BOLD) + "\n")
    sys.stderr.write(c("  ❯ ", GREEN))
    sys.stderr.flush()
    return input().strip()


# ─────────────────────────────────────────────────────────────
#  Banner
# ─────────────────────────────────────────────────────────────

def print_banner() -> None:
    banner_lines = [
        "",
        "  ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗     ██╗███████╗████████╗",
        "  ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║     ██║██╔════╝╚══██╔══╝",
        "  ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║     ██║███████╗   ██║   ",
        "  ██║███╗██║██║   ██║██╔══██╗██║  ██║██║     ██║╚════██║   ██║   ",
        "  ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗██║███████║   ██║   ",
        "   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚══════╝   ╚═╝   ",
        "",
    ]
    title   = "  H A C K R A C K   W O R D L I S T   G E N E R A T O R"
    tagline = "  HackRack Custom Module  |  Authorized use only."
    divider = "  " + "─" * 64

    sys.stderr.write("\n")
    sys.stderr.write(divider + "\n")
    for line in banner_lines:
        sys.stderr.write(c(line, CYAN, BOLD) + "\n")
    sys.stderr.write(c(title, YELLOW, BOLD) + "\n")
    sys.stderr.write(c(tagline, DIM) + "\n")
    sys.stderr.write(divider + "\n")
    sys.stderr.write("\n")


# ─────────────────────────────────────────────────────────────
#  Main menu
# ─────────────────────────────────────────────────────────────

MENU_ITEMS = [
    ("1", "Custom wordlist  — combine names, dates, numbers & symbols"),
    ("2", "Brute-force      — every combination of a character set"),
    ("3", "Mutate wordlist  — leet-speak, case variants, prefixes/suffixes"),
    ("0", "Exit"),
]


def print_menu() -> None:
    sys.stderr.write(c("  Select a mode:\n\n", BOLD))
    for key, description in MENU_ITEMS:
        sys.stderr.write(c(f"  [{key}]", YELLOW, BOLD) + c(f"  {description}\n", RESET))
    sys.stderr.write("\n")


def read_menu_choice() -> str:
    valid = {key for key, _ in MENU_ITEMS}
    while True:
        sys.stderr.write(c("  ❯ ", GREEN))
        sys.stderr.flush()
        choice = input().strip()
        if choice in valid:
            return choice
        sys.stderr.write(c(
            f"  [!] Invalid choice '{choice}' — enter one of: "
            f"{', '.join(k for k, _ in MENU_ITEMS)}\n", RED))


# ─────────────────────────────────────────────────────────────
#  Mode 1 — Collect strings
# ─────────────────────────────────────────────────────────────

def collect_strings() -> list[str]:
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Mode 1]  Custom Wordlist\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Enter strings one per line (names, words, usernames…)\n", CYAN))
    sys.stderr.write(c("  Press Enter on an empty line when done.\n\n", DIM))

    strings: list[str] = []
    while True:
        sys.stderr.write(c(f"  string [{len(strings) + 1}]: ", BOLD))
        sys.stderr.flush()
        value = input().strip()

        if value == "":
            if not strings:
                sys.stderr.write(c("  [!] Please enter at least one string.\n", RED))
                continue
            break

        if value in strings:
            sys.stderr.write(c(f"  [~] '{value}' already added — skipping.\n", YELLOW))
            continue

        strings.append(value)
        sys.stderr.write(c(f"  [+] Added: {value}\n", GREEN))

    sys.stderr.write("\n")
    sys.stderr.write(c(f"  [*] Strings collected ({len(strings)}):\n", BOLD))
    for s in strings:
        sys.stderr.write(c(f"      • {s}\n", CYAN))
    sys.stderr.write("\n")

    return strings


# ─────────────────────────────────────────────────────────────
#  Case + leet variation generators
# ─────────────────────────────────────────────────────────────

# Map of characters to their leet-speak substitutes.
# Values are lists — a character can have more than one substitute.
# Matching is done on the lowercase version of the character.
LEET_MAP: dict[str, list[str]] = {
    "a": ["@"],
    "e": ["3"],
    "i": ["1"],
    "o": ["0"],
    "s": ["$", "5"],   # two common substitutes
    "t": ["7"],
    "l": ["1"],
    "b": ["8"],
    "g": ["9"],
}


def case_variations(word: str) -> list[str]:
    """
    Return all 2^n upper/lower-case combinations for every alphabetic
    character in *word*.  Non-alpha characters are kept as-is.
    """
    alpha_indices = [i for i, ch in enumerate(word) if ch.isalpha()]
    if not alpha_indices:
        return [word]
    variants: list[str] = []
    for bits in itertools.product((str.lower, str.upper), repeat=len(alpha_indices)):
        chars = list(word)
        for bit_fn, idx in zip(bits, alpha_indices):
            chars[idx] = bit_fn(chars[idx])
        variants.append("".join(chars))
    return variants


def leet_variations(word: str) -> list[str]:
    """
    Return all 2^m subsets of leet substitutions for *word*,
    where m = number of characters that have a leet alternative.

    Each substitutable character can be either its original form
    or its leet replacement, independently of every other character.

    e.g. "ae" → ["ae", "a3", "@e", "@3"]
    """
    # Build per-position choices: [original_char, sub1, sub2, ...]
    leet_positions: list[tuple[int, list[str]]] = []
    for i, ch in enumerate(word):
        subs = LEET_MAP.get(ch.lower())
        if subs:
            leet_positions.append((i, [ch] + subs))

    if not leet_positions:
        return [word]

    indices   = [pos[0]     for pos in leet_positions]
    choices   = [pos[1]     for pos in leet_positions]

    variants: list[str] = []
    for combo in itertools.product(*choices):
        chars = list(word)
        for idx, chosen in zip(indices, combo):
            chars[idx] = chosen
        variants.append("".join(chars))
    return variants


def all_variations(word: str) -> list[str]:
    """
    Combine leet + case: first expand all leet subsets of *word*,
    then expand all case combinations for each leet form.
    Returns a deduplicated list preserving insertion order.
    """
    seen: set[str] = set()
    result: list[str] = []
    for leet_form in leet_variations(word):
        for variant in case_variations(leet_form):
            if variant not in seen:
                seen.add(variant)
                result.append(variant)
    return result


def save_string_cache(strings: list[str], path: str = "temp/string_cache.txt") -> int:
    """
    Generate all case + leet variants for every string, deduplicate
    globally, and write to *path*.  Returns total words written.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    seen: set[str] = set()
    words: list[str] = []
    for s in strings:
        for variant in all_variations(s):
            if variant not in seen:
                seen.add(variant)
                words.append(variant)

    with open(path, "w", encoding="utf-8") as fh:
        for w in words:
            fh.write(w + "\n")

    return len(words)


# ─────────────────────────────────────────────────────────────
#  Mode 1 — Date collection & expansion
# ─────────────────────────────────────────────────────────────

DATECACHE = "temp/date_cache.txt"


def collect_dates() -> list[tuple[int, int, int]]:
    """
    Prompt the user for dates in mm/dd/yyyy format, one per line.
    Returns a list of (month, day, year) tuples.
    An empty line finishes input; dates are optional.
    """
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 2/?]  Dates\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Enter dates one per line in mm/dd/yyyy format.\n", CYAN))
    sys.stderr.write(c("  Press Enter on an empty line to skip / finish.\n\n", DIM))

    dates: list[tuple[int, int, int]] = []
    raw_seen: set[str] = set()

    while True:
        sys.stderr.write(c(f"  date [{len(dates) + 1}]: ", BOLD))
        sys.stderr.flush()
        raw = input().strip()

        if raw == "":
            break

        # Validate format mm/dd/yyyy
        try:
            parts = raw.split("/")
            if len(parts) != 3:
                raise ValueError
            mm, dd, yyyy = int(parts[0]), int(parts[1]), int(parts[2])
            if not (1 <= mm <= 12 and 1 <= dd <= 31 and 1000 <= yyyy <= 9999):
                raise ValueError
        except ValueError:
            sys.stderr.write(c("  [!] Invalid format — use mm/dd/yyyy (e.g. 03/15/1990)\n", RED))
            continue

        key = f"{mm:02d}/{dd:02d}/{yyyy:04d}"
        if key in raw_seen:
            sys.stderr.write(c(f"  [~] '{key}' already added — skipping.\n", YELLOW))
            continue

        raw_seen.add(key)
        dates.append((mm, dd, yyyy))
        sys.stderr.write(c(f"  [+] Added: {key}\n", GREEN))

    if dates:
        sys.stderr.write("\n")
        sys.stderr.write(c(f"  [*] Dates collected ({len(dates)}):\n", BOLD))
        for mm, dd, yyyy in dates:
            sys.stderr.write(c(f"      • {mm:02d}/{dd:02d}/{yyyy:04d}\n", CYAN))
        sys.stderr.write("\n")
    else:
        sys.stderr.write(c("  [*] No dates entered — skipping date step.\n\n", DIM))

    return dates


def date_variants(mm: int, dd: int, yyyy: int) -> list[str]:
    """
    Expand one date into a comprehensive set of string representations,
    covering all common day, month, and year forms across multiple separators.
    """
    # ── Year forms ────────────────────────────────────────────
    yy_s   = f"{yyyy % 100:02d}"   # 90
    yyyy_s = f"{yyyy:04d}"         # 1990

    # ── Month forms ───────────────────────────────────────────
    MONTH_SHORT = ["jan","feb","mar","apr","may","jun",
                   "jul","aug","sep","oct","nov","dec"]
    MONTH_LONG  = ["january","february","march","april","may","june",
                   "july","august","september","october","november","december"]
    mon_low   = MONTH_SHORT[mm - 1]          # jan
    mon_tit   = mon_low.capitalize()         # Jan
    mon_up    = mon_low.upper()              # JAN
    month_low = MONTH_LONG[mm - 1]          # january
    month_tit = month_low.capitalize()      # January
    month_up  = month_low.upper()           # JANUARY

    month_forms = [
        f"{mm:02d}",   # 03
        str(mm),       # 3
        mon_low,       # jan
        mon_tit,       # Jan
        mon_up,        # JAN
        month_low,     # january
        month_tit,     # January
        month_up,      # JANUARY
    ]

    # ── Day forms ─────────────────────────────────────────────
    def ordinal(n: int) -> str:
        sfx = {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th")
        return f"{n}{sfx}"

    day_forms = [
        f"{dd:02d}",   # 15
        str(dd),       # 15  (same if no leading zero needed)
        ordinal(dd),   # 15th
    ]

    # ── Combinations across separators ────────────────────────
    separators = ["/", "-", ".", ""]
    results: list[str] = []

    for sep in separators:
        for mf in month_forms:
            for df in day_forms:
                for yf in [yyyy_s, yy_s]:
                    results.append(f"{df}{sep}{mf}{sep}{yf}")   # dd-mm-yyyy
                    results.append(f"{mf}{sep}{df}{sep}{yf}")   # mm-dd-yyyy
                    results.append(f"{yf}{sep}{mf}{sep}{df}")   # yyyy-mm-dd
                    results.append(f"{yf}{sep}{df}{sep}{mf}")   # yyyy-dd-mm

    # ── Standalone partial tokens ─────────────────────────────
    results += [
        yyyy_s,
        yy_s,
        f"{mm:02d}{yyyy_s}",
        f"{dd:02d}{mm:02d}",
        f"{mm:02d}{dd:02d}",
        ordinal(dd),
    ]
    results += month_forms   # jan, Jan, JAN, january … on their own

    return list(dict.fromkeys(results))


def save_date_cache(dates: list[tuple[int, int, int]],
                    path: str = DATECACHE) -> int:
    """
    Expand all dates into format variants, deduplicate, and write to *path*.
    Returns total words written.
    """
    if not dates:
        return 0

    os.makedirs(os.path.dirname(path), exist_ok=True)

    seen: set[str] = set()
    words: list[str] = []
    for mm, dd, yyyy in dates:
        for variant in date_variants(mm, dd, yyyy):
            if variant not in seen:
                seen.add(variant)
                words.append(variant)

    with open(path, "w", encoding="utf-8") as fh:
        for w in words:
            fh.write(w + "\n")

    return len(words)



STRING_CACHE = "temp/string_cache.txt"

# ─────────────────────────────────────────────────────────────
#  Mode 1 — Special character collection
# ─────────────────────────────────────────────────────────────

SPECIAL_CACHE = "temp/special_cache.txt"


def collect_specials() -> list[str]:
    """
    Ask the user for special characters to use (one per line or space-separated).
    Returns a deduplicated list of individual characters.
    Optional — pressing Enter skips this step.
    """
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 3/?]  Special Characters\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Enter special characters (one per line, or space-separated).\n", CYAN))
    sys.stderr.write(c("  Common examples: @ ! # $ % & * - _ + = ? ~\n", DIM))
    sys.stderr.write(c("  Press Enter on an empty line to skip / finish.\n\n", DIM))

    specials: list[str] = []
    seen: set[str] = set()

    while True:
        sys.stderr.write(c(f"  char [{len(specials) + 1}]: ", BOLD))
        sys.stderr.flush()
        raw = input().strip()

        if raw == "":
            break

        # Accept multiple chars on one line (space-separated or run together)
        candidates = raw.split() if " " in raw else list(raw)

        added = []
        for ch in candidates:
            for single in list(ch):          # handle run-together input like "@!#"
                if single in seen:
                    continue
                seen.add(single)
                specials.append(single)
                added.append(single)

        if added:
            sys.stderr.write(c(f"  [+] Added: {' '.join(added)}\n", GREEN))
        else:
            sys.stderr.write(c("  [~] All characters already added — skipping.\n", YELLOW))

    if specials:
        sys.stderr.write("\n")
        sys.stderr.write(c(f"  [*] Special characters collected ({len(specials)}): ", BOLD))
        sys.stderr.write(c("  ".join(specials) + "\n\n", CYAN))
    else:
        sys.stderr.write(c("  [*] No special characters entered — skipping.\n\n", DIM))

    return specials


def save_special_cache(specials: list[str],
                       path: str = SPECIAL_CACHE) -> int:
    """
    Write each special character as its own line in *path*.
    Returns total characters written.
    """
    if not specials:
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for ch in specials:
            fh.write(ch + "\n")
    return len(specials)




def mode_custom_wordlist() -> None:
    # Step 1: strings
    strings = collect_strings()
    sys.stderr.write(c("  [~] Generating string variants…\n", DIM))
    s_total = save_string_cache(strings, STRING_CACHE)
    sys.stderr.write(
        c(f"  [+] {s_total:,} variants → ", GREEN) + c(STRING_CACHE, BOLD, CYAN) + "\n\n"
    )

    # Step 2: dates
    dates = collect_dates()
    if dates:
        sys.stderr.write(c("  [~] Expanding date formats…\n", DIM))
        d_total = save_date_cache(dates)
        sys.stderr.write(
            c(f"  [+] {d_total:,} date tokens → ", GREEN) + c(DATECACHE, BOLD, CYAN) + "\n\n"
        )

    # Step 3: special characters
    specials = collect_specials()
    if specials:
        sp_total = save_special_cache(specials)
        sys.stderr.write(
            c(f"  [+] {sp_total} special chars → ", GREEN) + c(SPECIAL_CACHE, BOLD, CYAN) + "\n\n"
        )

    # Step 4: optional alphanumeric data
    optionals = collect_optionals()
    if optionals:
        op_total = save_optional_cache(optionals)
        sys.stderr.write(
            c(f"  [+] {op_total:,} optional tokens → ", GREEN) + c(OPTIONAL_CACHE, BOLD, CYAN) + "\n\n"
        )

    # Step 5: length range
    min_len, max_len = read_length_range()

    # Step 6: merge all caches → main_cache.txt
    total_merged = merge_caches()
    sys.stderr.write(
        c(f"  [+] {total_merged:,} unique tokens → ", GREEN)
        + c(MAIN_CACHE, BOLD, CYAN) + "\n\n"
    )

    # Step 7: generate final wordlist
    generate_wordlist(min_len, max_len)

    # Clean up temp cache files
    import shutil
    shutil.rmtree("temp", ignore_errors=True)
    sys.stderr.write(c("  [~] Temp cache cleared.\n\n", DIM))


# ─────────────────────────────────────────────────────────────
#  Mode 1 — Final wordlist generator
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR  = "output"
OUTPUT_FILE = "output/wordlist.txt"


def generate_wordlist(min_len: int, max_len: int,
                      cache: str = "temp/main_cache.txt",
                      output: str = "output/wordlist.txt") -> None:
    """
    Read all tokens from *cache* and generate every ordered combination
    (with repetition) whose concatenated length falls within [min_len, max_len].

    Algorithm: iterative DFS with early pruning.
      - max_depth is computed automatically as  max_len // shortest_token_len
      - A branch is pruned as soon as adding the shortest token would exceed max_len
      - No path that can never yield a valid word is explored

    Progress is printed live: words written, elapsed time, words/second,
    and a per-depth breakdown at the end.
    """
    import time

    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 7/7]  Generating Wordlist\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    # ── Load token pool ───────────────────────────────────────────────
    if not os.path.exists(cache):
        sys.stderr.write(c(f"  [!] Cache not found: {cache}\n", RED))
        return

    with open(cache, encoding="utf-8") as fh:
        tokens = [line.rstrip("\n") for line in fh if line.strip()]

    if not tokens:
        sys.stderr.write(c("  [!] Token pool is empty.\n", RED))
        return

    n            = len(tokens)
    min_tok_len  = min(len(t) for t in tokens)
    max_depth    = max_len // max(min_tok_len, 1)   # auto-calculated

    sys.stderr.write(c(f"  Token pool   : {n:,} tokens\n", BOLD))
    sys.stderr.write(c(f"  Shortest tok : {min_tok_len} char(s)\n", BOLD))
    sys.stderr.write(c(f"  Length range : {min_len} – {max_len} chars\n", BOLD))
    sys.stderr.write(c(f"  Max depth    : {max_depth} (auto)\n", BOLD))
    sys.stderr.write(c(f"  Output       : {output}\n\n", BOLD))

    # ── Generate via DFS + early pruning ─────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    seen:         set[str]        = set()
    written:      int             = 0
    depth_counts: dict[int, int]  = {}   # depth → words written

    # Stack items: (prefix_string, current_depth)
    # Start with each token as the first level
    stack: list[tuple[str, int]] = [(tok, 1) for tok in reversed(tokens)]

    REPORT_EVERY = 10_000   # update the progress line every N words
    t_start      = time.time()
    t_last       = t_start

    with open(output, "w", encoding="utf-8") as out_fh:

        while stack:
            prefix, depth = stack.pop()
            plen = len(prefix)

            # ── Emit if length in range ────────────────────────────
            if plen >= min_len:
                if prefix not in seen:
                    seen.add(prefix)
                    out_fh.write(prefix + "\n")
                    written += 1
                    depth_counts[depth] = depth_counts.get(depth, 0) + 1

                    if written % REPORT_EVERY == 0:
                        elapsed = time.time() - t_start
                        rate    = written / elapsed if elapsed > 0 else 0
                        sys.stderr.write(
                            c(f"\r  [~] depth={depth:<3} "
                              f"written={written:>10,} "
                              f"speed={rate:>9,.0f} w/s "
                              f"elapsed={elapsed:>6.1f}s",
                              CYAN))
                        sys.stderr.flush()

            # ── Prune: shortest token would push past max_len ──────
            if plen + min_tok_len > max_len:
                continue

            # ── Push children ──────────────────────────────────────
            next_depth = depth + 1
            for tok in reversed(tokens):
                new = prefix + tok
                if len(new) <= max_len:
                    stack.append((new, next_depth))

    # ── Final summary ─────────────────────────────────────────────
    elapsed = time.time() - t_start
    rate    = written / elapsed if elapsed > 0 else 0

    sys.stderr.write("\n\n")
    sys.stderr.write(c("  " + "─" * 64 + "\n", DIM))
    sys.stderr.write(c("  Generation complete\n\n", BOLD))
    sys.stderr.write(c(f"  Total written : {written:,} words\n", GREEN))
    sys.stderr.write(c(f"  Elapsed       : {elapsed:.1f}s\n", DIM))
    sys.stderr.write(c(f"  Avg speed     : {rate:,.0f} words/sec\n", DIM))
    sys.stderr.write(c(f"  Output file   : {output}\n\n", CYAN))

    sys.stderr.write(c("  Words by depth:\n", BOLD))
    for d in sorted(depth_counts):
        bar_len = min(30, depth_counts[d] * 30 // max(depth_counts.values(), default=1))
        bar = "█" * bar_len
        sys.stderr.write(
            c(f"    depth {d:>2}  ", DIM)
            + c(f"{bar:<30} ", CYAN)
            + c(f"{depth_counts[d]:>10,}\n", BOLD))
    sys.stderr.write("\n")


# ─────────────────────────────────────────────────────────────

MAIN_CACHE = "temp/main_cache.txt"

CALL_CACHES = [
    "temp/string_cache.txt",
    "temp/date_cache.txt",
    "temp/special_cache.txt",
    "temp/optional_cache.txt",
]


def merge_caches(output: str = MAIN_CACHE) -> int:
    """
    Read all temp cache files that exist, merge their lines,
    eliminate duplicates (preserving first-seen order), and
    write everything to *output* (temp/main_cache.txt).
    Returns total unique tokens written.
    """
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 6/6]  Merging caches\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n")

    seen: set[str] = set()
    tokens: list[str] = []

    for cache_path in CALL_CACHES:
        if not os.path.exists(cache_path):
            sys.stderr.write(c(f"  [~] {cache_path} not found — skipping.\n", DIM))
            continue
        count_before = len(tokens)
        with open(cache_path, encoding="utf-8") as fh:
            for line in fh:
                word = line.rstrip("\n")
                if word and word not in seen:
                    seen.add(word)
                    tokens.append(word)
        added = len(tokens) - count_before
        sys.stderr.write(
            c(f"  [+] {cache_path:<32} → ", DIM)
            + c(f"{added:>7,} tokens", CYAN) + "\n"
        )

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as fh:
        for w in tokens:
            fh.write(w + "\n")

    sys.stderr.write(
        c(f"\n  [*] Total unique tokens : ", BOLD)
        + c(f"{len(tokens):,}", YELLOW)
        + c(f"  →  {output}\n", DIM)
    )
    return len(tokens)


# ─────────────────────────────────────────────────────────────
#  Mode 1 — Optional alphanumeric collection
# ─────────────────────────────────────────────────────────────
#  Mode 1 — Length range
# ─────────────────────────────────────────────────────────────

def read_length_range() -> tuple[int, int]:
    """
    Ask the user for a length range in the format  min-max  (e.g. 8-9).
    Loops until valid input is supplied.
    Returns (min_len, max_len).
    """
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 5/5]  Word Length Range\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Enter the minimum and maximum word length as  min-max\n", CYAN))
    sys.stderr.write(c("  e.g.  8-9   means words between 8 and 9 characters.\n", DIM))
    sys.stderr.write(c("  Enter a single number to use the same value for both.\n\n", DIM))

    while True:
        sys.stderr.write(c("  length range: ", BOLD))
        sys.stderr.flush()
        raw = input().strip()

        # Allow  "8"  as shorthand for  "8-8"
        if raw.isdigit():
            raw = f"{raw}-{raw}"

        parts = raw.split("-")
        if len(parts) != 2:
            sys.stderr.write(c("  [!] Use format  min-max  (e.g. 8-9).\n", RED))
            continue

        try:
            mn, mx = int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            sys.stderr.write(c("  [!] Both values must be whole numbers.\n", RED))
            continue

        if mn < 1:
            sys.stderr.write(c("  [!] Minimum must be at least 1.\n", RED))
            continue

        if mx < mn:
            sys.stderr.write(c(f"  [!] Maximum ({mx}) must be ≥ minimum ({mn}).\n", RED))
            continue

        sys.stderr.write(
            c(f"\n  [*] Lengths: ", BOLD)
            + c(f"{mn}", CYAN) + c(" – ", RESET) + c(f"{mx}", CYAN)
            + c(f" characters\n\n", RESET)
        )
        return mn, mx



OPTIONAL_CACHE = "temp/optional_cache.txt"


def collect_optionals() -> list[str]:
    """
    Prompt for optional alphanumeric values (phone, vehicle, house numbers…)
    one per line.  Optional — pressing Enter skips.
    """
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Step 4/?]  Optional Alphanumeric Data\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Enter any alphanumeric identifiers, one per line:\n", CYAN))
    sys.stderr.write(c("  e.g. mobile: 0300-1234567  |  plate: ABC-123  |  house: 42A\n", DIM))
    sys.stderr.write(c("  Press Enter on an empty line to skip / finish.\n\n", DIM))

    values: list[str] = []
    seen: set[str] = set()

    while True:
        sys.stderr.write(c(f"  value [{len(values) + 1}]: ", BOLD))
        sys.stderr.flush()
        raw = input().strip()

        if raw == "":
            break

        if raw in seen:
            sys.stderr.write(c(f"  [~] '{raw}' already added — skipping.\n", YELLOW))
            continue

        seen.add(raw)
        values.append(raw)
        sys.stderr.write(c(f"  [+] Added: {raw}\n", GREEN))

    if values:
        sys.stderr.write("\n")
        sys.stderr.write(c(f"  [*] Values collected ({len(values)}):\n", BOLD))
        for v in values:
            sys.stderr.write(c(f"      • {v}\n", CYAN))
        sys.stderr.write("\n")
    else:
        sys.stderr.write(c("  [*] No values entered — skipping.\n\n", DIM))

    return values


def optional_variants(value: str) -> list[str]:
    """
    Generate every useful representation of an alphanumeric identifier.

    Transformations applied:
      • Original as entered
      • Separator-stripped  (removes spaces, hyphens, underscores, dots)
      • Uppercase / lowercase / title-case of each of the above
      • Digit-only substring (if mixed alphanumeric)
      • Alpha-only substring (if mixed alphanumeric)
    """
    import re

    results: list[str] = []

    # Base forms: original and stripped of common separators
    stripped = re.sub(r"[\s\-_\.]", "", value)
    bases = list(dict.fromkeys([value, stripped]))   # deduplicate if no separators

    for base in bases:
        for variant in [
            base,
            base.upper(),
            base.lower(),
            base.title(),
        ]:
            results.append(variant)

    # Digit-only and alpha-only substrings as standalone tokens
    digits_only = re.sub(r"[^\d]", "", stripped)
    alpha_only  = re.sub(r"[^A-Za-z]", "", stripped)

    if digits_only and digits_only != stripped:
        results.append(digits_only)

    if alpha_only and alpha_only != stripped:
        for variant in [alpha_only, alpha_only.upper(),
                        alpha_only.lower(), alpha_only.title()]:
            results.append(variant)

    return list(dict.fromkeys(results))


def save_optional_cache(values: list[str],
                        path: str = OPTIONAL_CACHE) -> int:
    """
    Expand each value into all representations, deduplicate, and write to *path*.
    Returns total words written.
    """
    if not values:
        return 0

    os.makedirs(os.path.dirname(path), exist_ok=True)

    seen: set[str] = set()
    words: list[str] = []
    for v in values:
        for variant in optional_variants(v):
            if variant not in seen:
                seen.add(variant)
                words.append(variant)

    with open(path, "w", encoding="utf-8") as fh:
        for w in words:
            fh.write(w + "\n")

    return len(words)


# ─────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
#  Mode 2 — Brute-force
# ─────────────────────────────────────────────────────────────

import string as _string
import time   as _time

CHARSETS: dict[str, str] = {
    "1": ("Lowercase letters    a–z",          _string.ascii_lowercase),
    "2": ("Uppercase letters    A–Z",          _string.ascii_uppercase),
    "3": ("Digits               0–9",          _string.digits),
    "4": ("Special characters   !@#…",         r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""),
    "5": ("Alphanumeric         a–z A–Z 0–9",   _string.ascii_letters + _string.digits),
    "6": ("All printable        a–z A–Z 0–9 !@#…",
                                               _string.ascii_letters + _string.digits +
                                               r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""),
    "7": ("Custom               enter your own charset", ""),
}

BF_OUTPUT = "output/bf_wordlist.txt"


def _select_charset() -> str:
    """Interactive charset picker. Returns the chosen character string."""
    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Mode 2]  Brute-Force\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    sys.stderr.write(c("  Select a character set:\n\n", BOLD))
    for key, (label, _) in CHARSETS.items():
        sys.stderr.write(c(f"  [{key}]", YELLOW, BOLD) + f"  {label}\n")
    sys.stderr.write("\n")

    while True:
        sys.stderr.write(c("  ❯ ", GREEN))
        sys.stderr.flush()
        choice = input().strip()
        if choice not in CHARSETS:
            sys.stderr.write(c(
                f"  [!] Enter a number 1–{len(CHARSETS)}.\n", RED))
            continue

        label, chars = CHARSETS[choice]

        if choice == "7":
            sys.stderr.write(c("  Enter your custom charset: ", BOLD))
            sys.stderr.flush()
            chars = input().strip()
            if not chars:
                sys.stderr.write(c("  [!] Charset cannot be empty.\n", RED))
                continue
            # Deduplicate while preserving order
            seen_ch: set[str] = set()
            chars = "".join(ch for ch in chars if not (ch in seen_ch or seen_ch.add(ch)))

        sys.stderr.write(
            c(f"\n  [*] Charset ({len(chars)} chars): ", BOLD)
            + c(f"{chars[:60]}{'…' if len(chars) > 60 else ''}\n\n", CYAN)
        )
        return chars


def mode_bruteforce() -> None:
    """Mode 2 — generate every character-level combination within a length range."""
    # ── Step 1: charset ──────────────────────────────────────────────
    chars = _select_charset()

    # ── Step 2: length range ─────────────────────────────────────────
    min_len, max_len = read_length_range()

    # ── Summary ──────────────────────────────────────────────────────
    total_candidates = sum(len(chars) ** l for l in range(min_len, max_len + 1))
    divider = "  " + "─" * 64
    sys.stderr.write(divider + "\n")
    sys.stderr.write(c(f"  Charset size : {len(chars)} chars\n", BOLD))
    sys.stderr.write(c(f"  Length range : {min_len} – {max_len}\n", BOLD))
    sys.stderr.write(c(f"  Combinations : {total_candidates:,}\n", BOLD))
    sys.stderr.write(c(f"  Output       : {BF_OUTPUT}\n", BOLD))
    sys.stderr.write(divider + "\n\n")

    if total_candidates > 100_000_000:
        sys.stderr.write(c(
            f"  [!] {total_candidates:,} combinations — this may take a long time.\n\n",
            YELLOW))

    # ── Generate ─────────────────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    written   = 0
    REPORT_EVERY = 100_000
    t_start   = _time.time()

    with open(BF_OUTPUT, "w", encoding="utf-8") as out_fh:
        for length in range(min_len, max_len + 1):
            count_this_len = len(chars) ** length
            sys.stderr.write(
                c(f"  [~] Length {length:>3} — {count_this_len:>15,} words\n", DIM))
            sys.stderr.flush()

            for combo in itertools.product(chars, repeat=length):
                word = "".join(combo)
                out_fh.write(word + "\n")
                written += 1

                if written % REPORT_EVERY == 0:
                    elapsed = _time.time() - t_start
                    rate    = written / elapsed if elapsed > 0 else 0
                    pct     = written / total_candidates * 100
                    sys.stderr.write(
                        c(f"\r  [~] {pct:5.1f}%  "
                          f"written={written:>12,}  "
                          f"speed={rate:>10,.0f} w/s  "
                          f"elapsed={elapsed:>6.1f}s",
                          CYAN))
                    sys.stderr.flush()

    elapsed = _time.time() - t_start
    rate    = written / elapsed if elapsed > 0 else 0
    sys.stderr.write(
        c(f"\r\n\n  [+] Done!  {written:,} words  →  ", GREEN)
        + c(BF_OUTPUT, BOLD, CYAN)
        + c(f"\n  Elapsed: {elapsed:.1f}s  |  Avg: {rate:,.0f} w/s\n\n", DIM)
    )


def main() -> None:
    print_banner()
    print_menu()
    choice = read_menu_choice()

# ─────────────────────────────────────────────────────────────
#  Mode 3 — Mutate wordlist
# ─────────────────────────────────────────────────────────────

import time as _time2

MUT_OUTPUT = "output/mutated_wordlist.txt"

# Common prefixes & suffixes used in password mutations
COMMON_PREFIXES = ["1", "12", "123", "!", "@", "#", "0", "00"]
COMMON_SUFFIXES = [
    "1", "12", "123", "1234", "12345", "123456",
    "!", "@", "#", "$", "!!", "123!", "1!", "@123",
    "69", "007", "786", "99", "00", "2024", "2025",
]


def _load_wordlist(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return [line.rstrip("\n") for line in fh if line.strip()]


def _ask_yes_no(question: str, default: bool = True) -> bool:
    hint = c("[Y/n]" if default else "[y/N]", DIM)
    sys.stderr.write(c(f"  {question} ", BOLD) + hint + " ")
    sys.stderr.flush()
    raw = input().strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes")


def mode_mutate() -> None:
    """Mode 3 — apply mutations to every word in a user-supplied wordlist."""
    import time

    divider = "  " + "─" * 64
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  [Mode 3]  Mutate Wordlist\n", YELLOW, BOLD))
    sys.stderr.write(divider + "\n\n")

    # ── Step 1: input file ───────────────────────────────────────────
    sys.stderr.write(c("  Enter path to the wordlist file to mutate:\n", CYAN))
    while True:
        sys.stderr.write(c("  file: ", BOLD))
        sys.stderr.flush()
        path = input().strip().strip('"').strip("'")
        if os.path.isfile(path):
            break
        sys.stderr.write(c(f"  [!] File not found: {path}\n", RED))

    words = _load_wordlist(path)
    sys.stderr.write(c(f"\n  [+] Loaded {len(words):,} words from '{path}'\n\n", GREEN))

    # ── Step 2: choose mutations ─────────────────────────────────────
    sys.stderr.write(c("  Select mutations to apply:\n\n", BOLD))
    do_case     = _ask_yes_no("Apply case variations? (raheel → Raheel, RAHEEL…)")
    do_leet     = _ask_yes_no("Apply leet substitutions? (a→@ e→3 s→$ …)")
    do_prefixes = _ask_yes_no("Add common prefixes?  (123raheel, !raheel…)")
    do_suffixes = _ask_yes_no("Add common suffixes?  (raheel123, raheel!…)")

    # Custom prefix / suffix
    custom_pre: list[str] = []
    custom_suf: list[str] = []
    if do_prefixes:
        sys.stderr.write(c(
            "\n  Add extra prefixes (comma-separated, or Enter to skip): ", BOLD))
        sys.stderr.flush()
        raw = input().strip()
        custom_pre = [v.strip() for v in raw.split(",") if v.strip()]

    if do_suffixes:
        sys.stderr.write(c(
            "  Add extra suffixes (comma-separated, or Enter to skip): ", BOLD))
        sys.stderr.flush()
        raw = input().strip()
        custom_suf = [v.strip() for v in raw.split(",") if v.strip()]

    prefixes = COMMON_PREFIXES + custom_pre if do_prefixes else []
    suffixes = COMMON_SUFFIXES + custom_suf if do_suffixes else []

    # ── Step 3: optional length filter ──────────────────────────────
    sys.stderr.write("\n")
    apply_len = _ask_yes_no("Filter output by length? (skip to keep all lengths)")
    if apply_len:
        min_len, max_len = read_length_range()
    else:
        min_len, max_len = 1, 10_000

    # ── Generate ─────────────────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sys.stderr.write("\n" + divider + "\n")
    sys.stderr.write(c("  Mutating…\n\n", DIM))

    seen:    set[str] = set()
    written: int      = 0
    REPORT   = 10_000
    t_start  = time.time()

    def _emit(word: str, fh) -> None:
        nonlocal written
        if min_len <= len(word) <= max_len and word not in seen:
            seen.add(word)
            fh.write(word + "\n")
            written += 1
            if written % REPORT == 0:
                elapsed = time.time() - t_start
                rate    = written / elapsed if elapsed > 0 else 0
                sys.stderr.write(
                    c(f"\r  [~] written={written:>10,}  "
                      f"speed={rate:>9,.0f} w/s  "
                      f"elapsed={elapsed:>6.1f}s", CYAN))
                sys.stderr.flush()

    with open(MUT_OUTPUT, "w", encoding="utf-8") as out_fh:
        for word in words:
            # Expand case + leet (uses existing all_variations())
            if do_case or do_leet:
                base_forms = all_variations(word) if (do_case and do_leet) \
                    else (case_variations(word) if do_case else leet_variations(word))
            else:
                base_forms = [word]

            for form in base_forms:
                _emit(form, out_fh)

                # Prefixes
                for pre in prefixes:
                    _emit(pre + form, out_fh)

                # Suffixes
                for suf in suffixes:
                    _emit(form + suf, out_fh)

                # Prefix + Suffix (both ends)
                for pre in prefixes:
                    for suf in suffixes:
                        _emit(pre + form + suf, out_fh)

    elapsed = time.time() - t_start
    rate    = written / elapsed if elapsed > 0 else 0

    sys.stderr.write("\n\n")
    sys.stderr.write(divider + "\n")
    sys.stderr.write(c("  Mutation complete\n\n", BOLD))
    sys.stderr.write(c(f"  Base words       : {len(words):,}\n", DIM))
    sys.stderr.write(c(f"  Unique mutations : {written:,}\n", GREEN))
    sys.stderr.write(c(f"  Elapsed          : {elapsed:.1f}s\n", DIM))
    sys.stderr.write(c(f"  Avg speed        : {rate:,.0f} words/sec\n", DIM))
    sys.stderr.write(c(f"  Output           : {MUT_OUTPUT}\n\n", CYAN))


def main() -> None:
    print_banner()
    print_menu()
    choice = read_menu_choice()

    if choice == "1":
        mode_custom_wordlist()
    elif choice == "2":
        mode_bruteforce()
    elif choice == "3":
        mode_mutate()
    elif choice == "0":
        sys.stderr.write(c("\n  Goodbye.\n\n", DIM))
        sys.exit(0)


if __name__ == "__main__":
    main()
