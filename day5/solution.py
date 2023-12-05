from typing import List, Tuple
import re


class CustomMap:
    def __init__(self, range_maps: List[Tuple[int]]) -> None:
        """
        (dest, source, range)
        """
        self.range_maps = range_maps

    def __getitem__(self, v: int) -> int:
        for pair in self.range_maps:
            if pair[1] <= v < pair[1] + pair[2]:
                return pair[0] + (v - pair[1])
        return v

    def __repr__(self) -> str:
        return str(self.range_maps)

    def __str__(self) -> str:
        return self


class Set:
    def __init__(self, start: int, range: int) -> None:
        # start inclusive
        self.start = start
        self.range = range

    @property
    def end(self):
        # end exclusive
        return self.start + self.range

    def __repr__(self) -> str:
        return str(f"({self.start}, {self.range}, {self.end})")

    def intersects_with(self, other) -> bool:
        if other.end <= self.start or other.start >= self.end:
            return False
        return True

    def union(self, other):
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        range = end - start
        return Set(start, range)

    def __lt__(self, other) -> bool:
        return self.start < other.start

    def __le__(self, other) -> bool:
        return self.start <= other.start

    def __gt__(self, other) -> bool:
        return self.start > other.start

    def __ge__(self, other) -> bool:
        return self.start >= other.start


class SetMap:
    def __init__(self, range_map: List[Tuple[int]]) -> None:
        """
        (dest, source, range)
        """
        self.range_map = range_map
        self.custom_map = CustomMap(range_map)

    def get_intersections(self, v: Set):
        output_sets = []
        for pair in self.range_map:
            start_set = Set(pair[1], pair[2])
            if v.intersects_with(start_set):
                # chunk v into separate sets
                # lt (where v.start < start_set.start)
                # eq (where start_set.start <= v.start < start_set.end)
                # gt (where v.end >= start_set.end)

                # do the easy part where they overlap
                start = max(start_set.start, v.start)
                end = min(start_set.end, v.end)
                easy_output_set = Set(start, end - start)
                easy_output_set.start = self.custom_map[easy_output_set.start]
                output_sets.append(easy_output_set)

                # do any part where v is less than start_set
                if v.start < start_set.start:
                    temp_set = Set(v.start, start_set.start - v.start)
                    temp_intersections = self.get_intersections(temp_set)
                    output_sets.extend(temp_intersections)

                # do any part where v is greater than start_set
                if v.end > start_set.end:
                    temp_set = Set(start_set.end, v.end - start_set.end)
                    temp_intersections = self.get_intersections(temp_set)
                    output_sets.extend(temp_intersections)

        if len(output_sets) != 0:
            return output_sets
        # return the thing mapped to itself (since this is what it means)
        return [v]

        # idea - store (range, start_num)
        # and then only add a new item to the list
        # when start_num+range overlaps with new items :>


def parse_input(lines: List[str]) -> Tuple[List[int], Tuple[int]]:
    def get_map(start_idx) -> Tuple[Tuple[int], int]:
        idx = start_idx
        pairs = []
        while idx < len(lines) and lines[idx] != "":
            pairs.append(tuple(list(map(lambda val: int(val), lines[idx].split(" ")))))
            idx += 1
        return pairs, idx

    seeds = list(
        map(
            lambda val: int(val),
            filter(
                lambda val: val != "", lines[0][lines[0].index(":") + 1 :].split(" ")
            ),
        )
    )

    maps = {}
    idx = 1
    while idx < len(lines):
        if lines[idx] != "":
            line_name = re.findall("(.*) map:", lines[idx])[0]
            idx += 1
            pairs, idx = get_map(idx)
            maps[line_name] = pairs
        else:
            idx += 1

    return seeds, maps


def part1(lines: List[str]) -> int:
    # source, destination, range
    seeds, maps = parse_input(lines)

    # format the way we need to format
    unique_values = seeds

    # pass through all the maps
    for m in maps.values():
        m = CustomMap(m)
        unique_values = list(map(lambda v: m[v], unique_values))

    return min(unique_values)


def part2(lines: List[str]) -> int:
    seeds, maps = parse_input(lines)

    # format the way we need to format
    unique_values = []
    for i in range(0, len(seeds), 2):
        unique_values.append(Set(seeds[i], seeds[i + 1]))
    print(unique_values)

    # pass through all the maps
    for m in maps.values():
        # print(m)
        # print(unique_values)
        m = SetMap(m)
        next_values: List[Set] = []
        for v in unique_values:
            next_values.extend(m.get_intersections(v))

        # filter values
        # so what we do is do O(nlogn + n) ~ O(nlogn)
        # first sort, then merge cnsecutives if possible
        # print("next values before reducing is", next_values)
        next_values.sort()
        unique_values = [next_values[0]]
        i = 1
        while i < len(next_values):
            if unique_values[-1].intersects_with(next_values[i]):
                unique_values[-1] = unique_values[-1].union(next_values[i])
            else:
                unique_values.append(next_values[i])
            i += 1

    best_val = float("inf")
    for val in unique_values:
        best_val = min(val.start, best_val)
    return best_val


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
