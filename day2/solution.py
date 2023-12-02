import re


def extract_items(line: str):
    def get_rgb(s: str):
        r = re.search("([0-9]*) red", s)
        g = re.search("([0-9]*) green", s)
        b = re.search("([0-9]*) blue", s)

        r = int(r.groups()[0]) if r else 0
        g = int(g.groups()[0]) if g else 0
        b = int(b.groups()[0]) if b else 0

        return r, g, b

    game_num = int(re.search("Game (.*):", line).groups()[0])

    rgbs = list(map(get_rgb, line.split(";")))
    return game_num, rgbs


def is_game_possible(line: str) -> int:
    """
    Returns the game number if it's possible, else 0
    """

    NUM_RED = 12
    NUM_GREEN = 13
    NUM_BLUE = 14

    game_num, rgbs = extract_items(line)
    for r, g, b in rgbs:
        if r > NUM_RED or g > NUM_GREEN or b > NUM_BLUE:
            return 0
    return game_num


def power_of_min_possible(line: str) -> int:
    """
    Returns the `power` (r*g*b) of a the minimum cubes
    required for a game
    """
    _, rgbs = extract_items(line)

    max_r, max_g, max_b = 0, 0, 0
    for r, g, b in rgbs:
        max_r = max(max_r, r)
        max_g = max(max_g, g)
        max_b = max(max_b, b)

    return max_r * max_g * max_b


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip()
    print(sum(map(is_game_possible, lines.split("\n"))))
    print(sum(map(power_of_min_possible, lines.split("\n"))))
