from typing import List
import numpy as np


def sum_parts(lines: List[str]) -> int:
    used_matrix = np.zeros((len(lines), len(lines[0])), dtype=np.bool_)

    def get_number(line_idx: int, idx: int) -> int:
        """
        Modifies `lines` while it extracts a number
        to prevent double-counting
        """
        # [min, max)
        min_idx, max_idx = idx, idx
        while min_idx - 1 >= 0 and lines[line_idx][min_idx - 1].isnumeric():
            min_idx -= 1
        while max_idx < len(lines[line_idx]) and lines[line_idx][max_idx].isnumeric():
            max_idx += 1

        num = int(lines[line_idx][min_idx:max_idx])
        used_matrix[line_idx, min_idx:max_idx] = True
        return num

    def search_surroundings(line_idx: int, idx: int) -> int:
        temp_sum = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                if (
                    (line_idx + row >= 0 and line_idx + row < len(lines))
                    and (idx + col >= 0 and idx + col < len(lines[line_idx + row]))
                    and lines[line_idx + row][idx + col].isnumeric()
                    and not used_matrix[line_idx + row, idx + col]
                ):
                    temp_sum += get_number(line_idx + row, idx + col)
        return temp_sum

    parts_sum = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != "." and not lines[i][j].isnumeric():
                # found a character
                parts_sum += search_surroundings(i, j)
    return parts_sum


def sum_gears(lines: List[str]) -> int:
    used_matrix = np.zeros((len(lines), len(lines[0])), dtype=np.bool_)

    def get_number(line_idx: int, idx: int) -> int:
        # [min, max)
        min_idx, max_idx = idx, idx
        while min_idx - 1 >= 0 and lines[line_idx][min_idx - 1].isnumeric():
            min_idx -= 1
        while max_idx < len(lines[line_idx]) and lines[line_idx][max_idx].isnumeric():
            max_idx += 1

        num = int(lines[line_idx][min_idx:max_idx])
        used_matrix[line_idx, min_idx:max_idx] = True  # flag it as used
        return num

    def search_surroundings(line_idx: int, idx: int) -> int:
        nums = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if (
                    (line_idx + row >= 0 and line_idx + row < len(lines))
                    and (idx + col >= 0 and idx + col < len(lines[line_idx + row]))
                    and lines[line_idx + row][idx + col].isnumeric()
                    and not used_matrix[line_idx + row, idx + col]
                ):
                    nums.append(get_number(line_idx + row, idx + col))
        used_matrix[:, :] = False  # since we can reuse gears, set everything to unused

        # restore original
        if len(nums) == 2:
            return nums[0] * nums[1]
        return 0

    parts_sum = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "*":
                # found a character
                parts_sum += search_surroundings(i, j)
    return parts_sum


if __name__ == "__main__":
    lines = open("input.txt").read().strip().split("\n")
    print(sum_parts(lines))
    print(sum_gears(lines))
