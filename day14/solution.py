from typing import List, Tuple


def tilt_up(lines: str) -> List[List[str]]:
    lines = lines.split("\n")
    tilted = list(map(lambda s: list(map(lambda c: c, s)), lines))

    for col in range(len(tilted[0])):
        highest_pos = 0
        for row in range(len(tilted)):
            if lines[row][col] == "#":
                highest_pos = row + 1
            if lines[row][col] == "O":
                tilted[row][col] = "."
                tilted[highest_pos][col] = "O"
                highest_pos += 1

    return tilted


def tilt_down(lines: str) -> List[List[str]]:
    lines = lines.split("\n")
    tilted = list(map(lambda s: list(map(lambda c: c, s)), lines))

    for col in range(len(tilted[0])):
        lowest_pos = len(tilted) - 1
        for row in range(len(tilted) - 1, -1, -1):
            if lines[row][col] == "#":
                lowest_pos = row - 1
            if lines[row][col] == "O":
                tilted[row][col] = "."
                tilted[lowest_pos][col] = "O"
                lowest_pos -= 1

    return tilted


def tilt_right(lines: str) -> List[List[str]]:
    lines = lines.split("\n")
    tilted = list(map(lambda s: list(map(lambda c: c, s)), lines))

    for row in range(len(tilted)):
        rightmost = len(tilted[0]) - 1
        for col in range(len(tilted[0]) - 1, -1, -1):
            if lines[row][col] == "#":
                rightmost = col - 1
            if lines[row][col] == "O":
                tilted[row][col] = "."
                tilted[row][rightmost] = "O"
                rightmost -= 1

    return tilted


def tilt_left(lines: str) -> List[List[str]]:
    lines = lines.split("\n")
    tilted = list(map(lambda s: list(map(lambda c: c, s)), lines))

    for row in range(len(tilted)):
        leftmost = 0
        for col in range(len(tilted[0])):
            if lines[row][col] == "#":
                leftmost = col + 1
            if lines[row][col] == "O":
                tilted[row][col] = "."
                tilted[row][leftmost] = "O"
                leftmost += 1

    return tilted


def part1(lines: List[str]) -> int:
    tilted_lines = tilt_up("\n".join(lines))

    ret = 0
    for row in range(len(lines)):
        ret += tilted_lines[row].count("O") * (len(lines) - row)
    return ret


def part2(lines: List[str]) -> int:
    def flatten_list(lines: List[List[str]]) -> str:
        return "\n".join(map(lambda row: "".join(row), lines))

    def one_cycle(lines: str) -> str:
        tilted = flatten_list(tilt_up(lines))
        tilted = flatten_list(tilt_left(tilted))
        tilted = flatten_list(tilt_down(tilted))
        tilted = flatten_list(tilt_right(tilted))
        return tilted

    def to_list(lines: str) -> List[List[str]]:
        return list(map(lambda s: list(map(lambda c: c, s)), lines.split("\n")))

    tilted = "\n".join(lines)

    first_glance = {}
    cycles = {}
    num_cycles = 1000000000
    i = 0
    while i != num_cycles:
        if tilted not in cycles:
            tilted = one_cycle(tilted)
            i += 1
        else:
            if cycles[tilted] + i <= num_cycles:
                i += cycles[tilted]
            else:
                tilted = one_cycle(tilted)
                i += 1

        if tilted in first_glance:
            if i + (i - first_glance[tilted]) <= num_cycles:
                cycles[tilted] = i - first_glance[tilted]
            else:
                # use a smaller cycle
                first_glance[tilted] = i
        else:
            first_glance[tilted] = i

    tilted = to_list(tilted)
    ret = 0
    for row in range(len(tilted)):
        ret += tilted[row].count("O") * (len(tilted) - row)

    return ret


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
