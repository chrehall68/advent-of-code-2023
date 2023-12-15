from typing import List, Tuple
from functools import lru_cache
from tqdm import tqdm

MAX_CACHE_SIZE = 1024


def parse_lines(lines: List[str]) -> Tuple[List[str], List[List[int]]]:
    ret_lines = []
    ret_counts = []
    for line in lines:
        l, c = line.split()
        ret_lines.append(l)
        ret_counts.append(list(map(int, c.split(","))))
    return ret_lines, ret_counts


@lru_cache(maxsize=MAX_CACHE_SIZE)
def is_valid_so_far(line: str, count: Tuple[int], cur_streak: int):
    consecutive = []
    cur_consecutive = cur_streak
    for i in range(len(line)):
        if line[i] == "#":
            cur_consecutive += 1
        else:
            if cur_consecutive != 0:
                consecutive.append(cur_consecutive)
            if line[i] == "?":
                # ended on a question mark
                # since it could be either another # or a .
                # go one less
                one_less = len(consecutive) - 1
                if one_less == -1:
                    return True

                if cur_consecutive == 0:
                    # was a string of '.' before the '?'
                    return tuple(consecutive) == count[: len(consecutive)]
                else:
                    # was something like "##?"
                    return (
                        count[:one_less] == tuple(consecutive[:-1])
                        and len(consecutive) <= len(count)
                        and count[one_less] >= consecutive[-1]
                    )
            # continue, was just a period
            cur_consecutive = 0

    # case where it ends on "#"
    if cur_consecutive != 0:
        consecutive.append(cur_consecutive)
        cur_consecutive = 0

    return tuple(consecutive) == count


@lru_cache(maxsize=MAX_CACHE_SIZE)
def get_cur_count(line: str, cur_streak: int) -> Tuple[Tuple[int], int]:
    """
    Returns used up counts as well as current count
    """
    consecutive = []
    cur_consecutive = cur_streak
    for i in range(len(line)):
        if line[i] == "#":
            cur_consecutive += 1
        else:
            if cur_consecutive != 0:
                consecutive.append(cur_consecutive)

            if line[i] == "?":
                if len(consecutive) == 0:
                    return [], 0

                if cur_consecutive == 0:
                    # was a string of '.' before the '?'
                    return consecutive, 0
                else:
                    # was something like '##?'
                    return consecutive[:-1], cur_consecutive

            cur_consecutive = 0
    if cur_consecutive != 0:
        consecutive.append(cur_consecutive)
        cur_consecutive = 0
    return consecutive, 0


@lru_cache(maxsize=MAX_CACHE_SIZE)
def recursive_sol(line: str, count: Tuple[int], cur_streak: int):
    # base cases
    if not is_valid_so_far(line, count, cur_streak):
        return 0
    if "?" not in line:
        return 1

    # try using a . and try using a #
    cur_counts, next_cur_streak = get_cur_count(line, cur_streak)
    next_count = list(count)
    for item in cur_counts:
        if next_count[0] == item:
            next_count.pop(0)
        else:
            raise Exception("this shouldn't happen!!!")
    next_count = tuple(next_count)

    first_idx = line.index("?")
    return recursive_sol(
        "." + line[first_idx + 1 :], next_count, next_cur_streak
    ) + recursive_sol("#" + line[first_idx + 1 :], next_count, next_cur_streak)


def part1(lines: List[str]) -> int:
    lines, counts = parse_lines(lines)
    temp = list(
        map(lambda i: recursive_sol(lines[i], tuple(counts[i]), 0), range(len(lines)))
    )
    return sum(temp)


def rec_sol_modified(*items):
    return recursive_sol(items[0], tuple(items[1]), items[2])


def part2(lines: List[str]) -> int:
    def unfold(line, count) -> Tuple[str, List[int]]:
        return "?".join([line] * 5), count * 5

    lines, counts = parse_lines(lines)
    lines_and_counts = list(map(unfold, lines, counts))

    temp = [0 for _ in range(len(lines_and_counts))]
    for i, val in enumerate(tqdm(lines_and_counts)):
        temp[i] = rec_sol_modified(*val, 0)
    return sum(temp)


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
