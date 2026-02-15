#!/usr/bin/env python3
"""
Filter PGN games by Elo difference between players.
Streams the PGN file game by game — handles any size database.
Interactive prompts with sensible defaults.
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


def parse_header(game_lines, tag):
    """Extract a header value from a list of game lines."""
    for line in game_lines:
        if line.startswith(f'[{tag} "'):
            match = re.search(rf'\[{tag}\s+"([^"]*)"\]', line)
            if match:
                return match.group(1)
        # Headers are at the top; stop once we hit a non-header line
        if not line.startswith("[") and line.strip():
            break
    return None


def get_elo(game_lines, color):
    """Get Elo rating for White or Black. Returns None if missing/invalid."""
    val = parse_header(game_lines, f"{color}Elo")
    if val and val.isdigit():
        return int(val)
    return None


def stream_games(pgn_path):
    """Yield one game at a time as a list of lines."""
    current_game = []
    in_game = False

    with open(pgn_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            # Detect start of a new game
            if line.startswith('[Event "'):
                if current_game:
                    yield current_game
                current_game = [line]
                in_game = True
            elif in_game:
                current_game.append(line)

    # Don't forget the last game
    if current_game:
        yield current_game


def main():
    print("\n=== PGN Elo Difference Filter ===\n")

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

    # --- Parameters ---
    min_diff = int(prompt("Minimum Elo difference", 200))

    use_range = prompt("At least one player in a specific Elo range? (y/n)", "y").lower()
    elo_low = None
    elo_high = None
    if use_range == "y":
        elo_low = int(prompt("  Lower bound", 1650))
        elo_high = int(prompt("  Upper bound", 1850))

    # --- Output choice (ask before scanning) ---
    print("\nHow do you want to save?")
    print("  1. All matching games in one file")
    print("  2. Split: stronger player wins / weaker player wins or draws")
    print("  3. Both")
    choice = prompt("Choice", "1")

    out_dir = os.path.dirname(pgn_path)

    # Open output files
    f_all = None
    f_strong = None
    f_weak = None

    if choice in ("1", "3"):
        f_all = open(os.path.join(out_dir, "filtered_all.pgn"), "w", encoding="utf-8")
    if choice in ("2", "3"):
        f_strong = open(os.path.join(out_dir, "stronger_wins.pgn"), "w", encoding="utf-8")
        f_weak = open(os.path.join(out_dir, "weaker_wins_or_draws.pgn"), "w", encoding="utf-8")

    # --- Scan and filter ---
    print("\nScanning games...")
    total = 0
    matched = 0
    skipped_no_elo = 0
    strong_count = 0
    weak_count = 0

    for game_lines in stream_games(pgn_path):
        total += 1
        if total % 100000 == 0:
            print(f"  ...processed {total} games so far ({matched} matches)")

        w_elo = get_elo(game_lines, "White")
        b_elo = get_elo(game_lines, "Black")

        if w_elo is None or b_elo is None:
            skipped_no_elo += 1
            continue

        diff = abs(w_elo - b_elo)
        if diff < min_diff:
            continue

        if elo_low is not None and elo_high is not None:
            w_in = elo_low <= w_elo <= elo_high
            b_in = elo_low <= b_elo <= elo_high
            if not w_in and not b_in:
                continue

        matched += 1
        game_text = "".join(game_lines).strip() + "\n\n"

        if f_all:
            f_all.write(game_text)

        if f_strong or f_weak:
            result = parse_header(game_lines, "Result")
            stronger_won = False
            if w_elo > b_elo and result == "1-0":
                stronger_won = True
            elif b_elo > w_elo and result == "0-1":
                stronger_won = True

            if stronger_won:
                strong_count += 1
                if f_strong:
                    f_strong.write(game_text)
            else:
                weak_count += 1
                if f_weak:
                    f_weak.write(game_text)

    # Close files
    for f in (f_all, f_strong, f_weak):
        if f:
            f.close()

    # --- Summary ---
    print(f"\nDone! Scanned {total} games total.")
    if skipped_no_elo:
        print(f"  ({skipped_no_elo} games skipped — missing Elo data)")
    print(f"  {matched} games matched criteria.")

    if choice in ("1", "3") and matched:
        print(f"  Saved {matched} games to filtered_all.pgn")
    if choice in ("2", "3"):
        if strong_count:
            print(f"  Saved {strong_count} games to stronger_wins.pgn")
        if weak_count:
            print(f"  Saved {weak_count} games to weaker_wins_or_draws.pgn")

    if not matched:
        print("No matching games found. Try adjusting your criteria.")


if __name__ == "__main__":
    main()
