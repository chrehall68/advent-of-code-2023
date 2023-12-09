from typing import List


def parse_lines(lines: List[str]) -> List[List[int]]:
    return list(map(lambda row: list(map(int, row.split(" "))), lines))


def get_history(seq: List[int]) -> List[List[int]]:
    difs = [seq]
    while len(difs) == 1 or any(map(lambda val: val != 0, difs[-1])):
        next_row = []
        for i in range(len(difs[-1]) - 1):
            # append the difference
            next_row.append(difs[-1][i + 1] - difs[-1][i])
        difs.append(next_row)
    return difs


def part1(lines: List[str]) -> int:
    def extrapolate(seq: List[int]) -> int:
        difs = get_history(seq)
        # reconstruct
        for i in range(len(difs) - 1, -1, -1):
            if i == len(difs) - 1:
                difs[i].append(0)
            else:
                difs[i].append(difs[i][-1] + difs[i + 1][-1])

        return difs[0][-1]

    seqs = parse_lines(lines)
    return sum(map(extrapolate, seqs))


def part2(lines: List[str]) -> int:
    def extrapolate(seq: List[int]) -> int:
        difs = get_history(seq)
        # reconstruct
        for i in range(len(difs) - 1, -1, -1):
            if i == len(difs) - 1:
                difs[i].insert(0, 0)
            else:
                difs[i].insert(0, difs[i][0] - difs[i + 1][0])
        return difs[0][0]

    seqs = parse_lines(lines)
    return sum(map(extrapolate, seqs))


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
