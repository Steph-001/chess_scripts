#!/usr/bin/env python3
"""
PGN Variation Expander

Takes a PGN file with variations and outputs a new PGN where each unique path
through the variation tree becomes a separate complete game.

This solves the problem where chess training software doesn't recognize 
transpositions and only drills one move order to reach the same position.
"""

import argparse
import chess.pgn
import io
from pathlib import Path
from typing import List, Optional


def find_position_in_mainline(game: chess.pgn.Game, board: chess.Board) -> Optional[chess.pgn.ChildNode]:
    """
    Find a node in the main line that matches the given board position.
    
    Args:
        game: The game to search
        board: The position to find
        
    Returns:
        Node in main line with matching position, or None
    """
    current = game
    
    # Traverse the main line only (first variation at each node)
    while current.variations:
        current = current.variations[0]
        if current.board() == board:
            return current
    
    return None


def get_continuation_from_node(node: chess.pgn.ChildNode) -> List[chess.pgn.ChildNode]:
    """
    Get all moves following a node in the main line.
    
    Args:
        node: Node to start from
        
    Returns:
        List of moves following this node in the main line
    """
    continuation = []
    current = node
    
    # Follow the main line (first variation)
    while current.variations:
        main_move = current.variations[0]
        continuation.append(main_move)
        current = main_move
    
    return continuation


def extract_all_paths(game: chess.pgn.Game, node: chess.pgn.GameNode, current_path: List[chess.pgn.ChildNode]) -> List[List[chess.pgn.ChildNode]]:
    """
    Recursively extract all unique paths through the game tree.
    
    When a variation ends, find if the resulting position exists in the main line,
    and if so, continue from that point.
    
    Args:
        game: The original game (needed to search main line)
        node: Current node in the game tree
        current_path: List of nodes representing the path from root to current node
        
    Returns:
        List of paths, where each path is a list of nodes from root to leaf
    """
    paths = []
    
    if not node.variations:
        # Leaf node - check if we can continue from main line
        if current_path:
            # Get the board position at the end of current path
            end_board = current_path[-1].board()
            
            # Try to find this position in the main line
            mainline_node = find_position_in_mainline(game, end_board)
            
            if mainline_node:
                # Continue with moves after this position in main line
                continuation = get_continuation_from_node(mainline_node)
                complete_path = current_path + continuation
                paths.append(complete_path)
            else:
                # No continuation found, path ends here
                paths.append(current_path)
        return paths
    
    # Process all variations at this node
    for variation in node.variations:
        new_path = current_path + [variation]
        sub_paths = extract_all_paths(game, variation, new_path)
        paths.extend(sub_paths)
    
    return paths


def create_game_from_path(original_game: chess.pgn.Game, path: List[chess.pgn.ChildNode]) -> chess.pgn.Game:
    """
    Create a new game from a path through the variation tree.
    
    Args:
        original_game: Original game with headers
        path: List of nodes representing a complete path
        
    Returns:
        New game with the same headers but only moves from the path
    """
    # Create new game with same headers
    new_game = chess.pgn.Game()
    
    # Copy all headers from original game
    for key, value in original_game.headers.items():
        new_game.headers[key] = value
    
    # Build the move sequence
    current_node = new_game
    for move_node in path:
        current_node = current_node.add_variation(move_node.move)
        
        # Copy comments and annotations if present
        if move_node.comment:
            current_node.comment = move_node.comment
        if hasattr(move_node, 'nags') and move_node.nags:
            current_node.nags = move_node.nags.copy()
    
    return new_game


def expand_variations(input_file: str, output_file: str) -> int:
    """
    Read PGN file and expand all variations into separate games.
    
    Args:
        input_file: Path to input PGN file
        output_file: Path to output PGN file
        
    Returns:
        Number of games written
    """
    games_written = 0
    
    with open(input_file, 'r', encoding='utf-8') as pgn_file:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            
            while True:
                # Read next game from input
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                
                # Extract all paths through the variation tree
                paths = extract_all_paths(game, game, [])
                
                if not paths:
                    # No moves in game, write it as-is
                    print(game, file=out_file, end="\n\n")
                    games_written += 1
                else:
                    # Create a separate game for each path
                    for path in paths:
                        new_game = create_game_from_path(game, path)
                        print(new_game, file=out_file, end="\n\n")
                        games_written += 1
    
    return games_written


def main():
    parser = argparse.ArgumentParser(
        description='Expand PGN variations into separate complete games.',
        epilog='Example: python expand_variations.py input.pgn -o output.pgn'
    )
    parser.add_argument('input', help='Input PGN file with variations')
    parser.add_argument('-o', '--output', required=True, help='Output PGN file')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found.")
        return 1
    
    try:
        games_written = expand_variations(args.input, args.output)
        print(f"Successfully expanded variations.")
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
        print(f"Games written: {games_written}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
