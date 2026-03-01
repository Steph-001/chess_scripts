#!/usr/bin/env python3
"""
filter_games.py — Filter PGN games by Elo difference and rating range.
Streams the file line by line — handles huge PGN files without memory issues.

Usage:
    filter_games [OPTIONS] [FILE]

Options:
    -h, --help      Show this help message
    FILE            Path to PGN file (prompted if not given)

Study modes:
    1. Stronger opponent
       One player in your Elo range, opponent N points HIGHER.
       Study how stronger players punish mistakes at your level.

    2. Weaker opponent
       One player in your Elo range, opponent N points LOWER.
       Study how players at your level handle weaker opposition.

    3. Your level
       Both players in your Elo range (small difference).
       See typical mistakes and patterns at your level.

    4. Target level
       Both players in a custom range you define.
       Study a different rating bracket entirely.

    5. Custom
       Set White Elo range, Black Elo range, and minimum difference
       independently. Maximum flexibility.

Output options:
    1. All matching games in one file
    2. Split: stronger player wins / weaker player wins or draws
    3. Both

Output files are saved in the same directory as the input PGN.

Examples:
    filter_games my_database.pgn
    filter_games /path/to/megabase.pgn
    filter_games
"""

import re
import sys
import os


def prompt(message, default=None):
    """Prompt user with optional default value."""
    if default is not None:
        raw = input(f"{message} [{default}]: ").strip()
        return raw if raw else str(default)
    return input(f"{message}: ").strip()


def parse_header_line(line):
    """Extract tag name and value from a PGN header line."""
    match = re.match(r'\[(\w+)\s+"([^"]*)"\]', line)
    if match:
        return match.group(1), match.group(2)
    return None, None


def game_iterator(pgn_path):
    """
    Yield (headers_dict, full_game_text) one game at a time.
    Streams the file — only one game in memory at a time.
    """
    current_lines = []
    headers = {}

    with open(pgn_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            stripped = line.strip()

            # New game starts with [Event
            if stripped.startswith('[Event '):
                if current_lines:
                    yield headers, "".join(current_lines)
                current_lines = []
                headers = {}

            # Parse header lines
            tag, value = parse_header_line(stripped)
            if tag:
                headers[tag] = value

            current_lines.append(line)

    # Last game
    if current_lines:
        yield headers, "".join(current_lines)


def get_elo(headers, color):
    """Get Elo rating for White or Black. Returns None if missing/invalid."""
    val = headers.get(f"{color}Elo", "")
    if val.isdigit():
        return int(val)
    return None


def save_pgn(games, filepath):
    """Save a list of game text strings to a PGN file."""
    with open(filepath, "w", encoding="utf-8") as f:
        for g in games:
            f.write(g.strip())
            f.write("\n\n")


def show_help():
    """Print the module docstring as help."""
    print(__doc__)
    sys.exit(0)


def get_study_mode():
    """Prompt for study mode and return filter parameters."""
    print("\nStudy mode:")
    print("  1. Stronger opponent (your range vs higher-rated)")
    print("  2. Weaker opponent (your range vs lower-rated)")
    print("  3. Your level (both players in your range)")
    print("  4. Target level (both players in a custom range)")
    print("  5. Custom (set everything manually)")
    mode = prompt("\nChoice", "1")

    if mode == "1":
        print("\n--- Stronger opponent ---")
        lo = int(prompt("Your Elo range — lower bound", 1650))
        hi = int(prompt("Your Elo range — upper bound", 1850))
        diff = int(prompt("Minimum Elo difference of opponent", 200))
        max_diff_str = prompt("Maximum Elo difference of opponent (Enter for none)", "none")
        max_diff = None if max_diff_str.lower() == "none" else int(max_diff_str)
        return {
            "mode": "stronger",
            "your_lo": lo,
            "your_hi": hi,
            "min_diff": diff,
            "max_diff": max_diff,
        }

    elif mode == "2":
        print("\n--- Weaker opponent ---")
        lo = int(prompt("Your Elo range — lower bound", 1650))
        hi = int(prompt("Your Elo range — upper bound", 1850))
        diff = int(prompt("Minimum Elo difference of opponent", 200))
        max_diff_str = prompt("Maximum Elo difference of opponent (Enter for none)", "none")
        max_diff = None if max_diff_str.lower() == "none" else int(max_diff_str)
        return {
            "mode": "weaker",
            "your_lo": lo,
            "your_hi": hi,
            "min_diff": diff,
            "max_diff": max_diff,
        }

    elif mode == "3":
        print("\n--- Your level ---")
        lo = int(prompt("Elo range — lower bound", 1650))
        hi = int(prompt("Elo range — upper bound", 1850))
        max_diff = int(prompt("Maximum Elo difference between players", 50))
        return {
            "mode": "your_level",
            "range_lo": lo,
            "range_hi": hi,
            "max_diff": max_diff,
        }

    elif mode == "4":
        print("\n--- Target level ---")
        lo = int(prompt("Elo range — lower bound", 1900))
        hi = int(prompt("Elo range — upper bound", 2100))
        max_diff = int(prompt("Maximum Elo difference between players", 50))
        return {
            "mode": "target_level",
            "range_lo": lo,
            "range_hi": hi,
            "max_diff": max_diff,
        }

    elif mode == "5":
        print("\n--- Custom ---")
        w_lo = int(prompt("White Elo — lower bound", 1))
        w_hi = int(prompt("White Elo — upper bound", 3000))
        b_lo = int(prompt("Black Elo — lower bound", 1))
        b_hi = int(prompt("Black Elo — upper bound", 3000))
        min_diff = int(prompt("Minimum Elo difference (0 for any)", 0))
        return {
            "mode": "custom",
            "w_lo": w_lo,
            "w_hi": w_hi,
            "b_lo": b_lo,
            "b_hi": b_hi,
            "min_diff": min_diff,
        }

    else:
        print("Invalid choice.")
        sys.exit(1)


def matches_filter(w_elo, b_elo, params):
    """Check if a game matches the filter parameters."""
    diff = abs(w_elo - b_elo)

    mode = params["mode"]

    if mode == "stronger":
        your_lo = params["your_lo"]
        your_hi = params["your_hi"]
        min_diff = params["min_diff"]
        max_diff = params.get("max_diff")
        # White in your range, Black is stronger
        if your_lo <= w_elo <= your_hi:
            d = b_elo - w_elo
            if d >= min_diff and (max_diff is None or d <= max_diff):
                return True
        # Black in your range, White is stronger
        if your_lo <= b_elo <= your_hi:
            d = w_elo - b_elo
            if d >= min_diff and (max_diff is None or d <= max_diff):
                return True
        return False

    elif mode == "weaker":
        your_lo = params["your_lo"]
        your_hi = params["your_hi"]
        min_diff = params["min_diff"]
        max_diff = params.get("max_diff")
        # White in your range, Black is weaker
        if your_lo <= w_elo <= your_hi:
            d = w_elo - b_elo
            if d >= min_diff and (max_diff is None or d <= max_diff):
                return True
        # Black in your range, White is weaker
        if your_lo <= b_elo <= your_hi:
            d = b_elo - w_elo
            if d >= min_diff and (max_diff is None or d <= max_diff):
                return True
        return False

    elif mode in ("your_level", "target_level"):
        range_lo = params["range_lo"]
        range_hi = params["range_hi"]
        max_diff = params["max_diff"]
        if range_lo <= w_elo <= range_hi and range_lo <= b_elo <= range_hi:
            if diff <= max_diff:
                return True
        return False

    elif mode == "custom":
        if not (params["w_lo"] <= w_elo <= params["w_hi"]):
            return False
        if not (params["b_lo"] <= b_elo <= params["b_hi"]):
            return False
        if diff < params["min_diff"]:
            return False
        return True

    return False


def get_output_choice():
    """Prompt for output format."""
    print("\nHow do you want to save?")
    print("  1. All matching games in one file")
    print("  2. Split: stronger player wins / weaker player wins or draws")
    print("  3. Both")
    return prompt("Choice", "1")


def save_results(matching, out_dir, choice):
    """Save results according to user's output choice."""
    if choice in ("1", "3"):
        out_path = os.path.join(out_dir, "filtered_all.pgn")
        save_pgn(matching, out_path)
        print(f"Saved {len(matching)} games to {out_path}")

    if choice in ("2", "3"):
        stronger_wins = []
        weaker_wins_or_draws = []

        for game_text in matching:
            # Re-parse headers from game text for result splitting
            w_elo = None
            b_elo = None
            result = None
            for line in game_text.split("\n"):
                stripped = line.strip()
                tag, value = parse_header_line(stripped)
                if tag == "WhiteElo" and value.isdigit():
                    w_elo = int(value)
                elif tag == "BlackElo" and value.isdigit():
                    b_elo = int(value)
                elif tag == "Result":
                    result = value
                if w_elo and b_elo and result:
                    break

            if w_elo is None or b_elo is None:
                weaker_wins_or_draws.append(game_text)
                continue

            stronger_won = False
            if w_elo > b_elo and result == "1-0":
                stronger_won = True
            elif b_elo > w_elo and result == "0-1":
                stronger_won = True

            if stronger_won:
                stronger_wins.append(game_text)
            else:
                weaker_wins_or_draws.append(game_text)

        if stronger_wins:
            out_path = os.path.join(out_dir, "stronger_wins.pgn")
            save_pgn(stronger_wins, out_path)
            print(f"Saved {len(stronger_wins)} games to {out_path}")

        if weaker_wins_or_draws:
            out_path = os.path.join(out_dir, "weaker_wins_or_draws.pgn")
            save_pgn(weaker_wins_or_draws, out_path)
            print(f"Saved {len(weaker_wins_or_draws)} games to {out_path}")

        if not stronger_wins and not weaker_wins_or_draws:
            print("No games to save.")


def main():
    # --- Help ---
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        show_help()

    print("\n=== PGN Elo Filter ===\n")

    # --- Input file ---
    if len(sys.argv) > 1:
        pgn_path = sys.argv[1]
    else:
        pgn_path = prompt("Enter path to PGN file (or filename if in current directory)")
    pgn_path = pgn_path.strip("'\"")
    if not os.path.isabs(pgn_path):
        pgn_path = os.path.join(os.getcwd(), pgn_path)
    if not os.path.isfile(pgn_path):
        print(f"Error: file not found: {pgn_path}")
        sys.exit(1)

    # --- Study mode ---
    params = get_study_mode()

    # --- Scan (streaming) ---
    print("\nScanning games...")
    matching = []
    total = 0
    skipped = 0

    for headers, game_text in game_iterator(pgn_path):
        total += 1
        if total % 100000 == 0:
            print(f"  ...scanned {total} games, {len(matching)} matches so far")

        w_elo = get_elo(headers, "White")
        b_elo = get_elo(headers, "Black")

        if w_elo is None or b_elo is None:
            skipped += 1
            continue

        if matches_filter(w_elo, b_elo, params):
            matching.append(game_text)

    print(f"\nScanned {total} games total.")
    if skipped:
        print(f"  ({skipped} skipped — missing Elo data)")
    print(f"Found {len(matching)} matching games.")

    if not matching:
        print("No matching games. Try adjusting your criteria.")
        sys.exit(0)

    # --- Output ---
    choice = get_output_choice()
    out_dir = os.path.dirname(pgn_path)
    save_results(matching, out_dir, choice)
    print("\nDone!")


if __name__ == "__main__":
    main()
