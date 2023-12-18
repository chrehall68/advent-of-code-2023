from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Coordinate:
    row: int
    col: int


def shoelace(vertices: List[Tuple[int, int]]) -> int:
    """
    2A = |x1 x2| + ... + |xn x1|
         |y1 y2|         |yn y1|
    """
    a = 0
    for i in range(len(vertices)):
        # let x = row and y = col
        x1y2 = vertices[i][0] * vertices[(i + 1) % len(vertices)][1]
        x2y1 = vertices[(i + 1) % len(vertices)][0] * vertices[i][1]
        a += x1y2 - x2y1
    return abs(a) / 2


def outline(lines: List[str], use_corrected: bool = False) -> List[Tuple[int, int]]:
    corners = [(0, 0)]

    dirs = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}
    corrected_dirs = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for line in lines:
        if not use_corrected:
            dir = dirs[line[0]]
            num = int(line.split()[1])
        else:
            color_code = line.split()[2].lstrip("(#").rstrip(")")
            num = int(color_code[:5], base=16)
            dir = dirs[corrected_dirs[color_code[5]]]
        corners.append((corners[-1][0] + dir[0] * num, corners[-1][1] + dir[1] * num))

    # shift corners to be all positive
    min_row = min(corners, key=lambda pair: pair[0])[0]
    min_col = min(corners, key=lambda pair: pair[1])[1]
    return list(map(lambda pair: (pair[0] + min_row, pair[1] + min_col), corners))


def get_boundary(vertices: List[Tuple[int, int]]) -> int:
    b = 0
    for i in range(len(vertices)):
        b += abs(vertices[i][0] - vertices[(i + 1) % len(vertices)][0])
        b += abs(vertices[i][1] - vertices[(i + 1) % len(vertices)][1])
    return b


def get_true_area(vertices: List[Tuple[int, int]]) -> int:
    # pick's theorem states A = i + b/2 - 1
    # where b == boundary points
    # A == area
    # i == interior points
    # thus i = A - b/2 + 1
    a = shoelace(vertices)
    b = get_boundary(vertices)
    i = a - b / 2 + 1

    # since we want to count the interior + boundary,
    # we just do b + i
    # make sure we got an integer
    ret = b + i
    assert ret % 1 == 0, ret

    return int(ret)


def part1(lines: List[str]) -> int:
    corners = outline(lines)
    return get_true_area(corners)


def part2(lines: List[str]) -> int:
    corners = outline(lines, use_corrected=True)
    return get_true_area(corners)


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
