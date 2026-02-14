#!/usr/bin/env python3
"""
Filter PGN games by Elo difference between players.
Interactive prompts with sensible defaults.
"""

import re
import sys
import os


def parse_header(game_text, tag):
    """Extract a header value from a PGN game string."""
    match = re.search(rf'\[{tag}\s+"([^"]*)"\]', game_text)
    return match.group(1) if match else None


def parse_games(pgn_path):
    """Split a PGN file into individual game strings."""
    with open(pgn_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Split on double newline followed by [Event which marks a new game
    # We keep the [Event tag with the game
    games = re.split(r'\n\n(?=\[Event\s)', content)

    # Filter out empty strings
    games = [g.strip() for g in games if g.strip()]
    return games


def get_elo(game_text, color):
    """Get Elo rating for White or Black. Returns None if missing/invalid."""
    val = parse_header(game_text, f"{color}Elo")
    if val and val.isdigit():
        return int(val)
    return None


def prompt(message, default=None):
    """Prompt user with optional default value."""
    if default is not None:
        raw = input(f"{message} [{default}]: ").strip()
        return raw if raw else str(default)
    return input(f"{message}: ").strip()


def save_pgn(games, filepath):
    """Save a list of game strings to a PGN file."""
    with open(filepath, "w", encoding="utf-8") as f:
        for g in games:
            f.write(g.strip())
            f.write("\n\n")


def main():
    print("\n=== PGN Elo Difference Filter ===\n")

    # --- Input file ---
    if len(sys.argv) > 1:
        pgn_path = sys.argv[1]
    else:
        pgn_path = prompt("Enter path to PGN file (or filename if in current directory)")
    pgn_path = pgn_path.strip("'\"")  # remove quotes if drag-dropped
    # Resolve relative to current working directory
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

    # --- Scan ---
    print("\nScanning games...")
    all_games = parse_games(pgn_path)
    print(f"Found {len(all_games)} games total.")

    matching = []
    skipped_no_elo = 0

    for game in all_games:
        w_elo = get_elo(game, "White")
        b_elo = get_elo(game, "Black")

        if w_elo is None or b_elo is None:
            skipped_no_elo += 1
            continue

        diff = abs(w_elo - b_elo)
        if diff < min_diff:
            continue

        # Elo range check: at least one player in range
        if elo_low is not None and elo_high is not None:
            w_in = elo_low <= w_elo <= elo_high
            b_in = elo_low <= b_elo <= elo_high
            if not w_in and not b_in:
                continue

        matching.append(game)

    print(f"Found {len(matching)} games matching criteria.")
    if skipped_no_elo:
        print(f"  ({skipped_no_elo} games skipped — missing Elo data)")

    if not matching:
        print("No matching games found. Try adjusting your criteria.")
        sys.exit(0)

    # --- Output ---
    print("\nHow do you want to save?")
    print("  1. All matching games in one file")
    print("  2. Split: stronger player wins / weaker player wins or draws")
    print("  3. Both")
    choice = prompt("Choice", "1")

    # Determine output directory (same as input file)
    out_dir = os.path.dirname(os.path.abspath(pgn_path))

    if choice in ("1", "3"):
        out_path = os.path.join(out_dir, "filtered_all.pgn")
        save_pgn(matching, out_path)
        print(f"Saved {len(matching)} games to {out_path}")

    if choice in ("2", "3"):
        stronger_wins = []
        weaker_wins_or_draws = []

        for game in matching:
            w_elo = get_elo(game, "White")
            b_elo = get_elo(game, "Black")
            result = parse_header(game, "Result")

            # Determine if the stronger player won
            stronger_won = False
            if w_elo > b_elo and result == "1-0":
                stronger_won = True
            elif b_elo > w_elo and result == "0-1":
                stronger_won = True

            if stronger_won:
                stronger_wins.append(game)
            else:
                weaker_wins_or_draws.append(game)

        if stronger_wins:
            out_path = os.path.join(out_dir, "stronger_wins.pgn")
            save_pgn(stronger_wins, out_path)
            print(f"Saved {len(stronger_wins)} games to {out_path}")

        if weaker_wins_or_draws:
            out_path = os.path.join(out_dir, "weaker_wins_or_draws.pgn")
            save_pgn(weaker_wins_or_draws, out_path)
            print(f"Saved {len(weaker_wins_or_draws)} games to {out_path}")


if __name__ == "__main__":
    main()
