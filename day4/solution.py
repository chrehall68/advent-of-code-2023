from typing import List
import math


def get_line_worth(line: str) -> int:
    winning, have = line.split("|")
    winning = winning[winning.index(":") + 1 :]
    winning_numbers = list(filter(lambda val: val != "", winning.split(" ")))
    have_numbers = list(filter(lambda val: val != "", have.split(" ")))

    total = 0.5
    for num in have_numbers:
        if num in winning_numbers:
            total *= 2

    return int(total)


def get_copied_count(lines: List[str]) -> int:
    count = [1] * len(lines)
    for i in range(len(lines)):
        worth = get_line_worth(lines[i])
        if worth != 0:
            n_matches = int(math.log(worth, 2)) + 1
            for x in range(1, n_matches + 1):
                count[i + x] += count[i]

    return sum(count)


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")

    print(sum(map(get_line_worth, lines)))
    print(get_copied_count(lines))
