
from typing import List, Optional, Tuple

Grid = List[List[int]]
Coord = Tuple[int, int]

def load_puzzle(filepath: str) -> Tuple[str, Grid]:
    """
    Load the sudoku puzzle from .txt files
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError(f"Puzzle file is empty: {filepath}")

    title = lines[0]
    grid_lines = lines[1:]

    if len(grid_lines) != 9 or any(len(row) != 9 for row in grid_lines):
        raise ValueError("Puzzle must contain a title line followed by a 9x9 grid.")

    grid: Grid = [[int(ch) for ch in row] for row in grid_lines]
    return title, grid

def is_valid_assignment(grid: Grid, row: int, col: int, num: int) -> bool:
    """
    Return true if placing 'num' at (row, col) violates no Sudoku constraints.
    """
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            if grid[r][c] == num:
                return False

    return True

def format_grid(grid: Grid) -> str:
    """
    Format a 9x9 board for the game grid. Use for console/.txt output.
    """
    rows_out = []
    for r in range(9):
        if r > 0 and r % 3 == 0:
            rows_out.append("-" * 21)
        row_items = []
        for c in range(9):
            if c > 0 and c % 3 == 0:
                row_items.append("|")
            val = grid[r][c]
            row_items.append(str(val) if val != 0 else ".")
        rows_out.append(" ".join(row_items))
    return "\n".join(rows_out)