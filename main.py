
import copy
from src.board import format_grid, load_puzzle
from src.naive_solver import solve_naive_algorithm

def main() -> None:
    title, initial_grid = load_puzzle("puzzles/sudoku_01.txt")
    working_grid = copy.deepcopy(initial_grid)
    print(f"--- {title} (Initial) ---")
    print(format_grid(initial_grid))
    solved, stats = solve_naive_algorithm(working_grid)

    print(f"\nSolved: {solved}")
    print(f"Time: {stats.elapsed_seconds:.6f}s | Number of Recursive Calls: {stats.recursive_calls} | Number of Backtracks: {stats.backtracks}")
    if solved:
        print(f"\n --- {title} (Solved) ---")
        print(format_grid(working_grid))

if __name__ == "__main__":
    main()