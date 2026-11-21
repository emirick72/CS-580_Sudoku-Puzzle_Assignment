
import copy
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple
from src.board import Grid, format_grid, load_puzzle
from src.naive_solver import SolverStats, solve_naive_algorithm
from src.smart_solver import SmartSolverStats, solve_smart_backtracking

SolverFn = Callable[[Grid], Tuple[bool, object]]

@dataclass
class BenchmarkRow:
    file: str
    title: str
    clues: int
    solver: str
    solved: bool
    valid_solution: bool
    elapsed_seconds: float
    recursive_calls: int
    backtracks: int
    domain_wipeouts: Optional[int]

def count_clues(grid: Grid) -> int:
    """
    Counts how many non-zeros numbers are in the initial grid
    """
    return sum(1 for row in grid for val in row if val != 0)

def is_valid_solution(initial_grid: Grid, solved_grid: Grid) -> bool:
    """
    Verify if there are completed rows, cols, and mini 3x3 grids
    """
    expected = set(range(1, 10))
    for r in range(9):
        if initial_grid[r][c] != 0 and solved_grid[r][c] != initial_grid[r][c]:
            return False

    for i in range(9):
        if {solved_grid[i][c] for c in range(9)} != expected:
            return False
        if {solved_grid[r][i] for r in range(9)} != expected:
            return False

    for box_r in range(0, 9, 3):
        for box_c in range(0, 9, 3):
            box_vals = {
                solved_grid[r][c]
                for r in range(box_r, box_r + 3)
                for c in range(box_c, box_c + 3)
            }
            if box_vals != expected:
                return False
    return True

def run_single_solver(
        filepath: Path,
        title: str,
        initial_grid: Grid,
        solver_name: str,
        solver_fn: SolverFn,
) -> Tuple[BenchmarkRow, Grid]:
    """
    Run one solver to solve all puzzles at the same time; collect results and store in a CSV file
    """
    working_grid = copy.deepcopy(initial_grid)
    solved, stats = solver_fn(working_grid)
    valid = is_valid_solution(initial_grid, working_grid) if solved else False

    if isinstance(stats, (SolverStats, SmartSolverStats)):
        elapsed = stats.elapsed_seconds
        calls = stats.recursive_calls
        backtracks = stats.backtracks
        wipeouts = (
            stats.domain_wipeouts if isinstance(stats, SmartSolverStats) else None
        )
    else:
        raise TypeError(f"Unexpected stats object returns by {solver_name}: {type(stats)}")

    row = BenchmarkRow(
        file=filepath.name,
        title=title,
        clues=count_clues(initial_grid),
        solver=solver_name,
        solved=solved,
        valid_solution=valid,
        elapsed_seconds=elapsed,
        recursive_calls=calls,
        backtracks=backtracks,
        domain_wipeouts=wipeouts
    )
    return row, working_grid

def run_benchmark(
        puzzles_dir: str = "puzzles",
        csv_output: Optional[str] = "benchmark_results.csv",
        print_solutions: bool = False
) -> List[BenchmarkRow]:
    """
    Run both naive and smart solvers for all puzzles and output results to a CSV file
    """
    puzzle_paths = sorted(Path(puzzles_dir).glob("*.txt"))
    if not puzzle_paths:
        raise FileNotFoundError(f"No .txt puzzle files found in '{puzzles_dir}'")
    rows: List[BenchmarkRow] = []

    solvers: List[Tuple[str, SolverFn]] = [
        ("Naive", solve_naive_algorithm)
        ("Smart (MRV, LCV, and FC)", solve_smart_backtracking)
    ]

    for path in puzzle_paths:
        title, inital_grid = load_puzzle(str(path))
        for solver_name, solver_fr in solvers:
            row, solved_grid = run_single_solver(
                path, title, initial_grid, solver_name, solver_fn
            )