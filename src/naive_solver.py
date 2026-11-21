
from dataclasses import dataclass
import time
from typing import Optional
from src.board import Coord, Grid, is_valid_assignment

@dataclass
class SolverStats:
    solved: bool
    elapsed_seconds: float
    recursive_calls: int
    backtracks: int

def find_next_empty_in_order(grid: Grid) -> Optional[Coord]:
    """
    Find the grid's first empty cell; function scans row by row and column by column
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return (r, c)
    return None

def solve_naive_algorithm(grid: Grid) -> tuple[bool, SolverStats]:
    """
    Solve the puzzle using naive backtracking alg.
    """
    start_time = time.perf_counter()
    recursive_calls = 0
    backtracks = 0

    def backtrack() -> bool:
        nonlocal recursive_calls, backtracks
        recursive_calls += 1

        empty = find_next_empty_in_order(grid)
        if empty is None:
            return True

        row, col = empty

        for num in range(1, 10):
            if is_valid_assignment(grid, row, col, num):
                grid[row][col] = num
                if backtrack():
                    return True
                grid[row][col] = 0
                backtracks += 1
        return False

    solved = backtrack()
    elapsed = time.perf_counter() - start_time
    stats = SolverStats(
        solved=solved,
        elapsed_seconds=elapsed,
        recursive_calls=recursive_calls,
        backtracks=backtracks
    )
    return solved, stats