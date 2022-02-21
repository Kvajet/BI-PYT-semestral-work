from typing import Tuple

import numpy as np

from app.src.level.Level import Level


class Astar:
    """Astar algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm.

    Pretty common algorithm which is used for finding a path.
    I use it as one type of enemy movement.
    """

    def __init__(self, level: Level):
        self._level = level

        self._g_score = np.full(self._level.size, 0, np.int16)
        self._f_score = np.full(self._level.size, 0, np.float16)
        self._came_from = np.full(
            (self._level.size[0], self._level.size[1], 2),
            -1,
            np.int16
        )
        self._open_set = set()

    def _reset_values(self) -> None:
        """Resets all arrays, fresh start for next search."""
        self._g_score = np.full(self._level.size, 1000000, np.int16)
        self._f_score = np.full(self._level.size, 1000000, np.float16)
        self._came_from = np.full(
            (self._level.size[0], self._level.size[1], 2),
            -1,
            np.int16
        )

    def _heuristic_function(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Heuristic function, specifically Manhattan function."""
        return abs(x1 - x2) + abs(y1 - y2)

    def _lowest_f_score(self) -> Tuple[int, int]:
        """Finds a node with lowest f_value. Important part of A*."""
        lowest = None
        for node in self._open_set:
            if not lowest:
                lowest = node
                continue
            if self._f_score[node] < self._f_score[lowest]:
                lowest = node
        return lowest

    def _process_neighbour(
        self,
        current: Tuple[int, int],
        neighbour: Tuple[int, int],
        fr: Tuple[int, int]
    ) -> None:
        """Solves one neighbour, checks if is valid and add other
        neighbours if they were not in _open_set yet."""
        if neighbour[0] < 0 or neighbour[0] >= self._level.size[0]:
            return
        if neighbour[1] < 0 or neighbour[1] >= self._level.size[1]:
            return
        if self._level.bool_layout[neighbour[1]][neighbour[0]]:
            return

        tentative_g_score = self._g_score[current] + 1
        if tentative_g_score < self._g_score[neighbour]:
            self._came_from[neighbour] = current
            self._g_score[neighbour] = tentative_g_score
            self._f_score[neighbour] = tentative_g_score
            + self._heuristic_function(*fr, *neighbour)

            if neighbour not in self._open_set:
                self._open_set.add(neighbour)

    def _reconstruct_path(
        self,
        current: Tuple[int, int]
    ) -> list[Tuple[int, int]]:
        """Reconstructs viable path and returns list of indices.
        """
        total_path: list[Tuple[int, int]] = []
        while current[0] >= 0 and current[1] >= 0:
            total_path.append(current)
            current = tuple(self._came_from[current])
        total_path.reverse()
        return total_path

    def find_path(
        self,
        fr: Tuple[int, int],
        to: Tuple[int, int]
    ) -> list[Tuple[int, int]]:
        """Core part of A*. Public function to be called."""
        self._reset_values()

        self._open_set = set({fr})

        self._g_score[fr] = 0
        self._f_score[fr] = self._heuristic_function(*fr, *to)

        while self._open_set:
            current = self._lowest_f_score()
            if current == to:
                return self._reconstruct_path(current)
            self._open_set.remove(current)

            self._process_neighbour(current, (current[0] - 1, current[1]), fr)
            self._process_neighbour(current, (current[0] + 1, current[1]), fr)
            self._process_neighbour(current, (current[0], current[1] - 1), fr)
            self._process_neighbour(current, (current[0], current[1] + 1), fr)

        return []
