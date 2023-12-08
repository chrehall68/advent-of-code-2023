from typing import List, Tuple
import re
import math


def parse_input(lines: List[str]) -> Tuple[List[int], dict]:
    instruction_map = {"L": 0, "R": 1}
    instruction = list(map(lambda val: instruction_map[val], lines[0]))

    ret = {}
    for line in lines[2:]:
        source = re.findall("(.*) =", line)[0]
        left = re.findall("\((.*),", line)[0]
        right = re.findall(", (.*)\)", line)[0]
        ret[source] = (left, right)
    # print(ret)
    return instruction, ret


def part1(lines: List[str]) -> int:
    instruction, d = parse_input(lines)
    cur = "AAA"
    cur_instruction = 0
    while cur != "ZZZ":
        cur = d[cur][instruction[cur_instruction % len(instruction)]]
        cur_instruction += 1
    return cur_instruction


def part2(lines: List[str]) -> int:
    def get_next(
        cur_instruction_mod: int,
        source: str,
    ) -> Tuple[str, int]:
        """
        Returns the next Z destination and how long it takes to get there
        """
        cur_times = 0
        cur = source
        while cur_times == 0 or not cur.endswith("Z"):
            cur = d[cur][
                instruction[(cur_instruction_mod + cur_times) % len(instruction)]
            ]
            cur_times += 1
        return cur, cur_times

    instruction, d = parse_input(lines)

    # basically, store how long it took to get there and each current
    cur = list(zip([0] * len(d), filter(lambda s: s.endswith("A"), d.keys())))
    while any(map(lambda v: v[0] == 0, cur)):
        pair = cur.pop(0)
        next_source, extra_times = get_next(pair[0] % len(instruction), pair[1])
        cur.append((pair[0] + extra_times, next_source))

    # all divisible by len(instructions)!!
    all_divisible = all(map(lambda v: v[0] % len(instruction) == 0, cur))

    # now calculate how long it takes to move everything 1 more time
    copy_cur = []
    # do one full iteration
    for pair in cur:
        next_source, extra_times = get_next(pair[0] % len(instruction), pair[1])
        copy_cur.append((pair[0] + extra_times, next_source))

    # all divisible!!
    all_divisible_2 = all(map(lambda v: v[0] % len(instruction) == 0, copy_cur))
    # all actually the same number as they were in cur
    all_same = all(map(lambda v, c: v[0] - c[0] == c[0], copy_cur, cur))

    # so all we gotta do is figure out what the initial values are // len(instruction)
    # then do lcm. This works for the actual input
    if all_divisible and all_divisible_2 and all_same:
        multipliers = list(map(lambda v: v[0] // len(instruction), cur))
        lcm = math.lcm(*multipliers)
        return lcm * len(instruction)

    # pass test case
    while any(map(lambda v: v[0] != cur[0][0], cur)):
        pair = min(cur)
        cur.remove(pair)
        next_source, extra_times = get_next(pair[0] % len(instruction), pair[1])
        cur.append((pair[0] + extra_times, next_source))
    return cur[0][0]


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
