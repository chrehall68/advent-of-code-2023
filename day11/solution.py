from typing import List, Tuple


def get_empty(lines: List[str]) -> Tuple[List[int], List[int]]:
    empty_rows = []
    empty_cols = []

    # find empty rows
    for idx, row in enumerate(lines):
        if "#" not in row:
            empty_rows.append(idx)

    # find empty cols
    for col in range(len(lines[0])):
        if all(map(lambda row: lines[row][col] != "#", range(len(lines)))):
            empty_cols.append(col)

    return empty_rows, empty_cols


def find_all(lines: List[str] | List[List[str]]) -> List[Tuple[int, int]]:
    # find all #'s
    locs = []
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "#":
                locs.append((row, col))
    return locs


def parse_input(lines: List[str]) -> List[List[str]]:
    ret = [list(map(lambda c: c, row)) for row in lines]

    empty_rows, empty_cols = get_empty(lines)

    # expand the rows (but do it backwards that way idxs are still valid)
    for row in reversed(empty_rows):
        ret.insert(row, ["."] * len(ret[row]))

    # expand the cols (but do it backwards that way idxs are still valid)
    for col in reversed(empty_cols):
        for row in range(len(ret)):
            ret[row].insert(col, ".")

    return ret


def part1(lines: List[str]) -> int:
    def manhattan_distance(loc_1: Tuple[int, int], loc_2: Tuple[int, int]):
        return abs(loc_1[0] - loc_2[0]) + abs(loc_1[1] - loc_2[1])

    parsed_lines = parse_input(lines)

    locs = find_all(parsed_lines)

    # get manhattan distance between each val and each other val
    ret = 0
    for i in range(len(locs)):
        ret += sum(map(lambda v: manhattan_distance(locs[i], v), locs[i + 1 :]))

    return ret


def part2(lines: List[str], multiplier: int = 1000000) -> int:
    empty_rows, empty_cols = get_empty(lines)

    def manhattan_distance(loc_1: Tuple[int, int], loc_2: Tuple[int, int]):
        total = 0

        # go through the rows
        for row in range(min(loc_1[0], loc_2[0]), max(loc_1[0], loc_2[0])):
            if row in empty_rows:
                total += multiplier
            else:
                total += 1

        # go through the cols
        for col in range(min(loc_1[1], loc_2[1]), max(loc_1[1], loc_2[1])):
            if col in empty_cols:
                total += multiplier
            else:
                total += 1

        return total

    locs = find_all(lines)

    ret = 0
    for i in range(len(locs)):
        ret += sum(map(lambda v: manhattan_distance(locs[i], v), locs[i + 1 :]))

    return ret


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
