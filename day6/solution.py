from typing import List, Tuple
import re


def parse_input(lines: List[str]) -> Tuple[map, map]:
    times = map(int, re.findall("([0-9]+)", lines[0]))
    distances = map(int, re.findall("([0-9]+)", lines[1]))
    return times, distances


def prod(*items: int):
    if items[0] == 0:
        return 0
    count = 1
    for item in items:
        count *= item
    return count


def get_num_ways(time: int, distance: int):
    count = 0
    for i in range(time):
        if i * (time - i) > distance:
            count += 1
    return count


def part1(lines: List[str]) -> int:
    times, distances = parse_input(lines)
    counts = list(map(lambda pair: get_num_ways(*pair), zip(times, distances)))
    return prod(*counts)


def part2(lines: List[str]) -> int:
    times, distances = parse_input(lines)
    times = int("".join(map(str, times)))
    distances = int("".join(map(str, distances)))
    return get_num_ways(times, distances)


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
