
import copy
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from src.board import Grid, format_grid, load_puzzle
from src.naive_solver import SolverStats, solve_naive_algorithm
from src.smart_solver import SmartSolverStats, solve_smart_backtracking

def run_benchmarch(
        puzzle_dir: str = "puzzles",
        output_file: str = "benchmark_results.txt"
) -> None:
    """
    Run naive and smart puzzle solvers; output results to a txt file
    """
    puzzle_paths = sorted(Path(puzzle_dir).glob("*.txt"))
    if not puzzle_paths:
        raise FileNotFoundError(f"No .txt file found for any puzzles in '{puzzle_dir}/'.")
    results: List[Tuple[str, str, Grid, Grid, SolverStats, SmartSolverStats]] = []

    for path in puzzle_paths:
        title, initial_grid = load_puzzle(str(path))
        print(f"Benchmarking {path.name} ({title})...")

        naive_grid = copy.deepcopy(initial_grid)
        _, naive_stats = solve_naive_algorithm(naive_grid)

        smart_grid = copy.deepcopy(initial_grid)
        _, smart_stats = solve_smart_backtracking(smart_grid)

        results.append(
            (path.name, title, initial_grid, smart_grid, naive_stats, smart_stats)
        )

    lines: List[str] = []
    lines.append("-" * 80)
    lines.append("SUDOKU CSP BENCHMARK FILE")
    lines.append("-" * 80)
    lines.append("")

    # COMPARISON TABLE HERE
    header = (
        f"{'Puzzle':<16} | {'Naive Time':>13} | {'Smart Time':>13} | "
        f"{'Naive Calls':>11} | {'Smart Calls':>11} | {'Naive Backtracking':>9} | {'Smart Backtracking':>9} | {'Wipeouts':>8}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for filename, title, _, _, naive_stats, smart_stats in results:
        label = f"{filename[:16]}"
        lines.append(
            f"{label:<16} | {naive_stats.elapsed_seconds:>14} | {smart_stats.elapsed_seconds:>14f} | "
            f"{naive_stats.recursive_calls:>11,d} | {smart_stats.recursive_calls:>11,d} | "
            f"{naive_stats.backtracks:>9,d} | {smart_stats.backtracks:>8,d} | {smart_stats.domain_wipeouts:>8,d}"
        )
    lines.append("")
    lines.append("=" * 80)
    lines.append("PUZZLE SOLUTIONS")
    lines.append("=" * 80)

    for filename, title, initial_grid, solved_grid, naive_stats, smart_stats in results:
        speedup = (
            naive_stats.elapsed_seconds / smart_stats.elapsed_seconds
            if smart_stats.elapsed_seconds > 0
            else float("inf")
        )
        lines.append("")
        lines.append(f"--- {title}: ({filename}) ---")
        lines.append(
            f"Naive: Solved={naive_stats.solved}, Time={naive_stats.elapsed_seconds:.6f}s, "
            f"Recursive Calls={naive_stats.recursive_calls:,d}, Number of Backtracks={naive_stats.backtracks:,d}"
        )
        lines.append(
            f"Smart: Solved={smart_stats.solved}, Time={smart_stats.elapsed_seconds:.6f}s, "
            f"Recursive Calls={smart_stats.recursive_calls:,d}, Number of Backtracks={smart_stats.backtracks:,d}, "
            f"Domain Wipeouts={smart_stats.domain_wipeouts:,d} ({speedup:.1f}x faster)"
        )
        lines.append("\nInitial Grid:")
        lines.append(format_grid(initial_grid))
        lines.append("\nSolved/Final Grid:")
        lines.append(format_grid(solved_grid))
        lines.append("-" * 45)

    report_text = "\n".join(lines) + "\n"
    print("\n" + report_text)
    Path(output_file).write_text(report_text, encoding="utf-8")
    print(f"Saved benchmark output to: {output_file}")

if __name__ == "__main__":
    run_benchmarch()