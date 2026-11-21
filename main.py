
import copy
from src.board import format_grid, load_puzzle
from src.naive_solver import solve_naive_algorithm
from src.smart_solver import solve_smart_backtracking

def main() -> None:
    title, initial_grid = load_puzzle("puzzles/sudoku_01.txt")
    print(f"--- {title} (Initial) ---")
    print(format_grid(initial_grid))

    naive_grid = copy.deepcopy(initial_grid)
    naive_ok, naive_stats = solve_naive_algorithm(naive_grid)
    print(
        f"\n[Naive] Solved={naive_ok} | Time={naive_stats.elapsed_seconds:.6f}s | "
        f"Recursive Calls={naive_stats.recursive_calls} | Backtracks={naive_stats.backtracks}"
    )

    smart_grid = copy.deepcopy(initial_grid)
    smart_ok, smart_stats = solve_smart_backtracking(smart_grid)
    print(
        f"[Smart] Solved={smart_ok} | Time={smart_stats.elapsed_seconds:.6f}s | "
        f"Recursive Calls={smart_stats.recursive_calls} | Backtracks={smart_stats.backtracks} | "
        f"Wipeouts={smart_stats.domain_wipeouts}"
    )

    if smart_ok:
        print(f"\n--- {title} (Solved) ---")
        print(format_grid(smart_grid))


if __name__ == "__main__":
    main()