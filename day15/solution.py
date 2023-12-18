from typing import List
from collections import OrderedDict


def hash(section: str) -> int:
    ret = 0
    for char in section:
        ret += ord(char)
        ret *= 17
        ret %= 256
    return ret


def part1(lines: List[str]) -> int:
    assert len(lines) == 1
    return sum(map(hash, lines[0].split(",")))


def part2(lines: List[str]) -> int:
    m = {i: OrderedDict() for i in range(256)}
    assert len(lines) == 1
    lines = lines[0]
    for item in lines.split(","):
        letters = "".join(filter(lambda c: c.isalpha(), item))
        letters_hash = hash(letters)

        operation = item[len(letters)]
        if operation == "-":
            if letters in m[letters_hash]:
                del m[letters_hash][letters]
        else:
            m[letters_hash][letters] = int(item[len(letters) + 1 :])

    ret = 0
    for box_num in range(256):
        box = m[box_num]
        for i, focal_len in enumerate(box.values()):
            ret += (box_num + 1) * (i + 1) * focal_len
    return ret


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
