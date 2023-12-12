from typing import List, Tuple


def parse_input(lines: List[str]) -> Tuple[str, Tuple[int, int], List[List[str]]]:
    # figure out where the start is
    start_pos = (-1, -1)
    for i in range(len(lines)):
        if "S" in lines[i]:
            start_pos = (i, lines[i].index("S"))
            break

    # figure out what the pipe is
    # connects is in row, col
    connects = {
        (-1, 0): {"|", "7", "F"},  # upper connects
        (1, 0): {"|", "L", "J"},  # lower connects
        (0, 1): {"-", "J", "7"},  # right connects
        (0, -1): {"-", "L", "F"},  # left connects
    }
    dirs = []
    for dir in connects.keys():
        if lines[start_pos[0] + dir[0]][start_pos[1] + dir[1]] in connects[dir]:
            dirs.append(dir)
    outputs = {
        ((1, 0), (0, 1)): "F",  # connects below and right
        ((-1, 0), (1, 0)): "|",  # connects up
        ((0, 1), (0, -1)): "-",  # connects sideways
        ((1, 0), (0, -1)): "7",  # down and left
        ((-1, 0), (0, 1)): "L",
        ((-1, 0), (0, -1)): "J",
    }
    return (
        outputs[tuple(dirs)],
        start_pos,
        list(map(lambda row: list(map(lambda c: c, row)), lines)),
    )


def part1(lines: List[str]) -> int:
    real_tube, start_pos, lines = parse_input(lines)
    lines[start_pos[0]][start_pos[1]] = real_tube
    cur_pos = start_pos
    count = 0

    connect_dirs = {
        # vertical
        ((-1, 0), "|"): (-1, 0),
        ((1, 0), "|"): (1, 0),
        # horizontal
        ((0, -1), "-"): (0, -1),
        ((0, 1), "-"): (0, 1),
        # L's
        ((1, 0), "L"): (0, 1),
        ((0, -1), "L"): (-1, 0),
        # F's
        ((-1, 0), "F"): (0, 1),
        ((0, -1), "F"): (1, 0),
        # 7's
        ((-1, 0), "7"): (0, -1),
        ((0, 1), "7"): (1, 0),
        # J's
        ((1, 0), "J"): (0, -1),
        ((0, 1), "J"): (-1, 0),
    }

    cur_dir = None
    for pair in connect_dirs.keys():
        if real_tube in pair[1]:
            cur_dir = pair[0]
            break

    while count == 0 or cur_pos != start_pos:
        output_dir = connect_dirs[(cur_dir, lines[cur_pos[0]][cur_pos[1]])]
        cur_dir = output_dir
        cur_pos = (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1])
        count += 1

    return count // 2


def part2(lines: List[str]) -> int:
    real_tube, start_pos, lines = parse_input(lines)
    lines[start_pos[0]][start_pos[1]] = real_tube
    floodfilled_lines = list(
        map(lambda v: list(map(lambda v: ".", range(len(lines[0])))), range(len(lines)))
    )
    bool_lines = list(
        map(lambda v: list(map(lambda v: ".", range(len(lines[0])))), range(len(lines)))
    )

    # first, trace the tube
    cur_pos = start_pos
    count = 0
    connect_dirs = {
        # vertical
        ((-1, 0), "|"): (-1, 0),
        ((1, 0), "|"): (1, 0),
        # horizontal
        ((0, -1), "-"): (0, -1),
        ((0, 1), "-"): (0, 1),
        # L's
        ((1, 0), "L"): (0, 1),
        ((0, -1), "L"): (-1, 0),
        # F's
        ((-1, 0), "F"): (0, 1),
        ((0, -1), "F"): (1, 0),
        # 7's
        ((-1, 0), "7"): (0, -1),
        ((0, 1), "7"): (1, 0),
        # J's
        ((1, 0), "J"): (0, -1),
        ((0, 1), "J"): (-1, 0),
    }

    cur_dir = None
    for pair in connect_dirs.keys():
        if real_tube in pair[1]:
            cur_dir = pair[0]
            break

    while count == 0 or cur_pos != start_pos:
        output_dir = connect_dirs[(cur_dir, lines[cur_pos[0]][cur_pos[1]])]
        cur_dir = output_dir
        cur_pos = (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1])
        count += 1

        bool_lines[cur_pos[0]][cur_pos[1]] = "1"
        floodfilled_lines[cur_pos[0]][cur_pos[1]] = lines[cur_pos[0]][cur_pos[1]]

    # get min and max
    min_row, max_row, min_col, max_col = float("inf"), 0, float("inf"), 0
    for row in range(len(bool_lines)):
        if "1" in bool_lines[row]:
            min_row = min(row, min_row)
            max_row = max(row, max_row)
            first_col = "".join(bool_lines[row]).find("1")
            last_col = "".join(bool_lines[row]).rfind("1")
            min_col = min(min_col, first_col)
            max_col = max(max_col, last_col)

    floodfilled_lines = list(
        map(
            lambda row: floodfilled_lines[row][min_col : max_col + 1],
            range(min_row, max_row + 1),
        )
    )

    # now for every thing shoot a ray and see what happens
    # if intersections % 2 == 1 => inside
    # else, outside
    def is_inside(row, col):
        # just shoot up (meaning we have to check left or right)
        direction = (-1, 0)
        cur_pos = (row, col)

        # if on the leftmost, it's already outside
        if cur_pos[1] == 0:
            return 0

        parallels = {"|", "J", "F", "L", "7"}
        count = 0
        while cur_pos[0] > -1:
            if floodfilled_lines[cur_pos[0]][cur_pos[1]] != ".":
                # check if it's parallel
                if floodfilled_lines[cur_pos[0]][cur_pos[1]] not in parallels:
                    count += 1
                # if it's doing a turn
                if (
                    floodfilled_lines[cur_pos[0]][cur_pos[1]] == "J"
                    or floodfilled_lines[cur_pos[0]][cur_pos[1]] == "7"
                ) and (
                    floodfilled_lines[cur_pos[0]][cur_pos[1] - 1] == "-"
                    or floodfilled_lines[cur_pos[0]][cur_pos[1] - 1] == "F"
                    or floodfilled_lines[cur_pos[0]][cur_pos[1] - 1] == "L"
                ):
                    count += 1

            cur_pos = (cur_pos[0] + direction[0], cur_pos[1] + direction[1])
        return count % 2

    # now actually run that
    count = 0
    stored = []
    for row in range(len(floodfilled_lines)):
        for col in range(len(floodfilled_lines[row])):
            if floodfilled_lines[row][col] == ".":
                temp = is_inside(row, col)
                count += temp
                if temp == 1:
                    stored.append((row, col))

    # print out
    # for item in stored:
    #     floodfilled_lines[item[0]][item[1]] = "#"
    # print("\n".join(map(lambda r: "".join(r), floodfilled_lines)))

    return count


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
