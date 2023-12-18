from typing import List, Tuple
import heapq


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class DirectionMap:
    def __init__(self) -> None:
        self.values = [0 for _ in range(len(directions))]
        self.key_to_index = {dir: i for i, dir in enumerate(directions)}

    def __getitem__(self, value):
        return self.values[self.key_to_index[value]]

    def __setitem__(self, key, value):
        self.values[self.key_to_index[key]] = value

    def __lt__(self, other):
        return self.values < other.values

    def __eq__(self, other) -> bool:
        return self.values == other.values

    def __hash__(self) -> int:
        return hash(tuple(self.values))

    def __repr__(self) -> str:
        return (
            str(self.cur_direction)
            + ":"
            + str(self[self.cur_direction])
            + f"({self.values})"
        )

    @property
    def cur_direction(self) -> Tuple[int, int]:
        if all(map(lambda v: v == 0, self.values)):
            return (0, 0)
        idx = next(filter(lambda i: self.values[i] != 0, range(len(self.values))))
        key = next(filter(lambda k: self.key_to_index[k] == idx, self.key_to_index))
        return key


def limited_dijkstra(
    lines: List[str], max_consecutive: int = 3, initial_increment: int = 1
) -> int:
    """
    Unfortunately, we can't just have an explored set since the number of
    times we've been going in that direction plays a role. Thus, the most
    we can do is try to prune and optimize with a heap
    """

    def is_opposite_dir(dir_a: Tuple[int, int], dir_b: Tuple[int, int]) -> bool:
        return (dir_a[0] == -dir_b[0] and abs(dir_a[0]) == 1) or (
            dir_a[1] == -dir_b[1] and abs(dir_a[1]) == 1
        )

    lines = list(map(lambda row: list(map(lambda c: int(c), row)), lines))
    grid = [[float("inf") for _ in range(len(lines[0]))] for _ in range(len(lines))]
    used_directions = [[[] for _ in range(len(lines[0]))] for _ in range(len(lines))]

    start = (0, 0)
    end = (len(lines) - 1, len(lines[0]) - 1)
    heap = [(0, start, DirectionMap())]
    cost, cur, dirs = heap.pop()
    i = 0

    while cur != end:
        cur_direction = dirs.cur_direction

        # add neighbors to heap or not
        for direction in directions:
            # if it's in the grid
            if dirs[direction] != 0:
                next_cur = cur[0] + direction[0], cur[1] + direction[1]
            else:
                next_cur = (
                    cur[0] + direction[0] * initial_increment,
                    cur[1] + direction[1] * initial_increment,
                )
            if (
                0 <= next_cur[0] < len(lines)
                and 0 <= next_cur[1] < len(lines[0])
                and not is_opposite_dir(cur_direction, direction)
            ):
                if dirs[direction] != 0:
                    if dirs[direction] < max_consecutive:
                        next_direction = DirectionMap()
                        next_direction[direction] = dirs[direction] + 1
                        next_cost = cost + lines[next_cur[0]][next_cur[1]]
                        if (next_cost < grid[next_cur[0]][next_cur[1]]) or (
                            next_direction not in used_directions[cur[0]][cur[1]]
                        ):
                            heapq.heappush(
                                heap,
                                (
                                    next_cost,
                                    next_cur,
                                    next_direction,
                                ),
                            )
                            grid[next_cur[0]][next_cur[1]] = min(
                                grid[next_cur[0]][next_cur[1]], next_cost
                            )
                            used_directions[cur[0]][cur[1]].append(next_direction)
                else:
                    next_direction = DirectionMap()
                    next_direction[direction] = initial_increment
                    next_cost = cost + sum(
                        map(
                            lambda i: lines[cur[0] + direction[0] * (i + 1)][
                                cur[1] + direction[1] * (i + 1)
                            ],
                            range(initial_increment),
                        )
                    )

                    if next_cost < grid[next_cur[0]][next_cur[1]] or (
                        next_direction not in used_directions[cur[0]][cur[1]]
                    ):
                        heapq.heappush(
                            heap,
                            (
                                next_cost,
                                next_cur,
                                next_direction,
                            ),
                        )
                        grid[next_cur[0]][next_cur[1]] = min(
                            grid[next_cur[0]][next_cur[1]], next_cost
                        )
                        used_directions[cur[0]][cur[1]].append(next_direction)

        # get next
        cost, cur, dirs = heapq.heappop(heap)
        i += 1

    return grid[end[0]][end[1]]


def part1(lines: List[str]) -> int:
    return limited_dijkstra(lines)


def part2(lines: List[str]) -> int:
    return limited_dijkstra(lines, max_consecutive=10, initial_increment=4)


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
