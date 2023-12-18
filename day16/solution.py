from typing import List, Tuple


def part1(lines: List[str], cur_pt: Tuple[int, int] = (0, 0), cur_dir="right") -> int:
    # convert to list of lists
    lines = list(map(lambda row: list(map(lambda c: c, row)), lines))
    direction_grid = [[set() for _ in range(len(lines[0]))] for _ in range(len(lines))]
    tiles = [[False for _ in range(len(lines[0]))] for _ in range(len(lines))]
    cur_stack = [(cur_pt, cur_dir)]

    def trace(cur_pt: Tuple[int, int], cur_dir: str):
        while (
            0 <= cur_pt[0] < len(lines)
            and 0 <= cur_pt[1] < len(lines[0])
            and cur_dir not in direction_grid[cur_pt[0]][cur_pt[1]]
        ):
            # record our direction
            direction_grid[cur_pt[0]][cur_pt[1]].add(cur_dir)

            # mark tile as energized
            tiles[cur_pt[0]][cur_pt[1]] = True

            # cases
            if lines[cur_pt[0]][cur_pt[1]] == ".":
                pass
            if lines[cur_pt[0]][cur_pt[1]] == "-":
                if cur_dir == "right" or cur_dir == "left":
                    pass
                else:
                    # use the left one
                    cur_dir = "left"
                    cur_stack.append((cur_pt, "right"))
            if lines[cur_pt[0]][cur_pt[1]] == "|":
                if cur_dir == "up" or cur_dir == "down":
                    pass
                else:
                    # use the up one
                    cur_dir = "up"
                    cur_stack.append((cur_pt, "down"))
            if lines[cur_pt[0]][cur_pt[1]] == "/":
                m = {"right": "up", "down": "left", "up": "right", "left": "down"}
                cur_dir = m[cur_dir]
            if lines[cur_pt[0]][cur_pt[1]] == "\\":
                m = {"right": "down", "up": "left", "down": "right", "left": "up"}
                cur_dir = m[cur_dir]

            # move current ray
            m = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
            movement = m[cur_dir]
            cur_pt = (cur_pt[0] + movement[0], cur_pt[1] + movement[1])

    while len(cur_stack) != 0:
        cur_pt, cur_dir = cur_stack.pop()

        trace(cur_pt, cur_dir)

    return sum(map(lambda row: row.count(True), tiles))


def part2(lines: List[str]) -> int:
    max_tiles = 0
    for row in range(len(lines)):
        max_tiles = max(
            part1(lines, (row, 0), "right"),
            part1(lines, (row, len(lines[0]) - 1), "left"),
            max_tiles,
        )
    for col in range(len(lines[0])):
        max_tiles = max(
            part1(lines, (0, col), "down"),
            part1(lines, (len(lines) - 1, col), "up"),
            max_tiles,
        )
    return max_tiles


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
