from typing import List, Tuple
from collections import Counter


class Hand:
    order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self, hand: str) -> None:
        self.hand = hand
        # val, count
        self.most_common = Counter(hand).most_common()
        self.hand_order = list(map(self.order.index, self.hand))

    @property
    def counts(self):
        return list(map(lambda pair: pair[1], self.most_common))

    def __lt__(self, other) -> bool:
        if self.counts == other.counts:
            # we want the first letter to be lower in order
            return self.hand_order < other.hand_order
        return self.counts > other.counts  # we want all the counts to be greater


class HandV2(Hand):
    order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    def __init__(self, hand: str) -> None:
        super().__init__(hand)

        # J's only rly have an effect if J wasn't the only item
        if "J" in hand and len(self.most_common) > 1:
            j_val = next(filter(lambda pair: pair[0] == "J", self.most_common))
            self.most_common.remove(j_val)

            self.most_common[0] = (
                self.most_common[0][0],
                # add the number of j's to the max val
                self.most_common[0][1] + j_val[1],
            )


def compare_hands(hands: List[str], bids: List[int], hand_type: type) -> List[int]:
    """
    Reorders bids in the order that the hands are
    """
    hands = sorted(
        zip(hands, bids),
        key=lambda pair: hand_type(pair[0]),
    )
    # print(hands)
    return list(map(lambda pair: pair[1], hands))


def parse_input(lines: List[str]) -> Tuple[List[str], List[int]]:
    hands = []
    bids = []
    for line in lines:
        line = line.split(" ")
        hands.append(line[0])
        bids.append(int(line[1]))
    return hands, bids


def part1(lines: List[str]) -> int:
    hands, bids = parse_input(lines)
    bids = compare_hands(hands, bids, hand_type=Hand)
    return sum(map(lambda pair: pair[1] * (len(bids) - pair[0]), enumerate(bids)))


def part2(lines: List[str]) -> int:
    hands, bids = parse_input(lines)
    bids = compare_hands(hands, bids, hand_type=HandV2)
    return sum(map(lambda pair: pair[1] * (len(bids) - pair[0]), enumerate(bids)))


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
