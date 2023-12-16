from typing import List, Tuple


def is_col_reflection(m: List[List[str]], i: int) -> Tuple[bool, List[List[bool]]]:
    """
    Returns:
        - bool - whether or not the column is a perfect reflection
        - List[List[int]] - list of differences (True means difference). Outer list is the column, inner list is the rows
            that differed for that column
    """
    # reflection on col 'i' means in the space before the col
    all_difs = []
    ret = True

    for col in range(min(i, len(m[0]) - i)):
        difs = list(map(lambda row: row[i - col - 1] != row[i + col], m))
        if any(difs):
            ret = False
        all_difs.append(difs)
    return ret, all_difs


def is_row_reflection(m: List[List[str]], i: int) -> Tuple[bool, List[List[bool]]]:
    """
    Returns:
        - bool - whether or not the row is a perfect reflection
        - List[List[int]] - list of differences (True means difference). Outer list is the row, inner list is the columns
            that differed for that row
    """
    # reflection on row 'i' means in the space before the row
    all_difs = []
    ret = True

    for row in range(min(i, len(m) - i)):
        # if the rows aren't equal
        difs = list(map(lambda c1, c2: c1 != c2, m[i - row - 1], m[i + row]))
        if any(difs):
            ret = False
        all_difs.append(difs)
    return ret, all_difs


def search_col_reflections(m: List[str], cols_to_exclude: List[int] = []) -> int:
    lines_reflected = 0
    count = 0
    for col in range(1, len(m[0])):
        if col in cols_to_exclude:
            continue
        if is_col_reflection(m, col)[0]:
            lines_reflected += col
            count += 1
    assert count <= 1
    return lines_reflected


def search_row_reflections(m: List[str], rows_to_exclude: List[int] = []) -> int:
    lines_reflected = 0
    count = 0
    for row in range(1, len(m)):
        if row in rows_to_exclude:
            continue
        if is_row_reflection(m, row)[0]:
            # number of rows above the line
            lines_reflected += row
    assert count <= 1
    return lines_reflected


def part1(lines: List[str]) -> int:
    ret = 0
    for m in lines:
        split_m = m.split("\n")
        cols_reflected = search_col_reflections(split_m)
        rows_reflected = search_row_reflections(split_m) * 100
        ret += cols_reflected + rows_reflected

        # there is only one line of reflection per thing
        assert not (cols_reflected != 0 and rows_reflected != 0)
    return ret


def part2(lines: List[str]) -> int:
    opposite_chars = {".": "#", "#": "."}

    cols_to_exclude = []
    rows_to_exclude = []

    def get_col_difs(m: List[str]):
        potentials = []
        for col in range(1, len(m[0])):
            valid, difs = is_col_reflection(m, col)
            if valid:
                cols_to_exclude.append(col)

            temp = [item for l in difs for item in l]
            if temp.count(True) == 1:  # there was only one difference
                # get the (row, col) version of the item
                rc = (-1, -1)
                for c in range(len(difs)):
                    for r in range(len(difs[c])):
                        if difs[c][r]:
                            assert rc == (-1, -1)
                            rc = (r, col - c - 1)

                potentials.append((col, rc, opposite_chars[m[rc[0]][rc[1]]]))
        return potentials

    def get_row_difs(m: List[str]):
        potentials = []
        for row in range(1, len(m)):
            valid, difs = is_row_reflection(m, row)
            if valid:
                rows_to_exclude.append(row)

            temp = [item for l in difs for item in l]
            if temp.count(True) == 1:  # there was only one difference
                # get the (row, col) version of the item
                rc = (-1, -1)
                for r in range(len(difs)):
                    for c in range(len(difs[r])):
                        if difs[r][c]:
                            assert rc == (-1, -1)
                            rc = (row - r - 1, c)
                potentials.append((row, rc, opposite_chars[m[rc[0]][rc[1]]]))
        return potentials

    ret = 0
    for m in lines:
        split_m = m.split("\n")
        potential_cols = get_col_difs(split_m)
        potential_rows = get_row_difs(split_m)
        assert (len(potential_rows) == 1 and len(potential_cols) == 0) or (
            len(potential_cols) == 1 and len(potential_rows) == 0
        )
        if len(potential_rows) != 0:
            item = potential_rows[0]
            ret += item[0] * 100
        if len(potential_cols) != 0:
            item = potential_cols[0]
            ret += item[0]
    return ret


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n\n")
    print(part1(lines))
    print(part2(lines))
