
from dataclasses import dataclass
import time
from typing import Dict, List, Optional, Set, Tuple
from src.board import Coord, Grid

DomainMap = Dict[Coord, Set[int]]

@dataclass
class SmartSolverStats:
    solved: bool
    elapsed_seconds: float
    recursive_calls: int
    backtracks: int
    domain_wipeouts: int

def build_peers() -> Dict[Coord, List[Coord]]:
    """
    Precompute the 20 peer coordinates from all cells
    """
    peers: Dict[Coord, List[Coord]] = {}
    for r in range(9):
        for c in range(9):
            peer_set: Set[Coord] = set()
            if i != c:
                peer_set.add((r, i))
            if i != r:
                peer_set.add((i, c))

        box_r0, box_c0 = (r // 3) * 3, (c // 3) * 3
        for br in range(box_r0, box_r0 + 3):
            for bc in range(box_c0, box_c0 + 3):
                if (br, bc) != (r, c):
                    peer_set.add((br, bc))
        peers[(r, c)] = sorted(peer_set)
    return peers

PEERS: Dict[Coord, List[Coord]] = build_peers()

def initialize_domains(grid: Grid) -> Optional[DomainMap]:
    """
    Build initial domains for all empty cells
    """
    domains: DomainMap = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                used = {
                    grid[pr][pc]
                    for (pr, pc) in PEERS[(r, c)]
                    if grid[pr][pc] != 0
                }
                candidates = set(range(1, 10)) - used
                if not candidates:
                    return None
                domains[(r, c)] = candidates
    return domains

def select_mrv_variable(domains: DomainMap) -> Coord:
    """
    Select the unassigned cell with the minimum remaining values (MRV)/smallest domain
    """
    return min(domains.keys(), key=lambda cell: len(domains[cell]))

def order_lcv_values(cell: Coord, domains: DomainMap) -> List[int]:
    """
    Order candidate values for 'cell' by least constraining value (LCV).
    Fewest value removals come first.
    """
    candidates = list(domains[cell])

    def eliminated_peer_choices(val: int) -> int:
        eliminated = 0
        for peer in PEERS[cell]:
            if peer in domains and val in domains[peer]:
                eliminated += 1
        return eliminated
    candidates.sort(key=eliminated_peer_choices)
    return candidates

def clone_domains(domains: DomainMap) -> DomainMap:
    """
    Copy domain sets so fail branches are discarded
    """
    return {cell: set(vals) for cell, vals in domains.items()}

def solve_smart_backtracking(grid: Grid) -> Tuple[bool, SmartSolverStats]:
    """
    Solve the grid in place using backtracking with MRV, LCV, and forward checking.
    """
    start_time = time.perf_counter()
    recursive_calls = 0
    backtracks = 0
    domain_wipeouts = 0

    initial_domains = initialize_domains(grid)
    if initial_domains is None:
        elapsed = time.perf_counter() - start_time
        return False, SmartSolverStats(False, elapsed, 0, 0, 0)

    def backtrack(current_domains: DomainMap) -> bool:
        nonlocal recursive_calls, backtracks, domain_wipeouts
        recursive_calls += 1

        if not current_domains:
            return True

        cell = select_mrv_variable(current_domains)
        r, c = cell

        for val in order_lcv_values(cell, current_domains):
            next_domains = clone_domains(current_domains)
            del next_domains[cell]
            wipeout = False
            for peer in PEERS[cell]:
                if peer in next_domains and val in next_domains[peer]:
                    next_domains[peer].remove(val)
                    if len(next_domains[peer]) == 0:
                        wipeout = True
                        domain_wipeouts += 1
                        break
            if wipeout:
                continue
            grid[r][c] = val
            if backtrack(next_domains):
                return True
            grid[r][c] = 0
            backtracks += 1
        return False

    solved = backtrack(initial_domains)
    elapsed = time.perf_counter() - start_time
    stats = SmartSolverStats(
        solved=solved,
        elapsed_seconds=elapsed,
        recursive_calls=recursive_calls,
        backtracks=backtracks,
        domain_wipeouts=domain_wipeouts
    )
    return solved, stats