def parse_line_v1(line: str) -> int:
    first_digit = -1
    second_digit = -1
    for char in line:
        if char.isdigit():
            if first_digit == -1:
                first_digit = int(char)
                second_digit = int(char)
            else:
                second_digit = int(char)
    return first_digit * 10 + second_digit


def parse_line_v2(line: str) -> int:
    m = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    m2 = {str(i): i for i in range(1, 10)}
    m.update(m2)

    first_digit = -1
    first_digit_index = float("inf")
    second_digit = -1
    second_digit_index = -1

    for key, val in m.items():
        if key in line:
            lowest_idx = line.find(key)
            highest_idx = line.rfind(key)

            if lowest_idx < first_digit_index:
                first_digit_index = lowest_idx
                first_digit = val
            if highest_idx > second_digit_index:
                second_digit_index = highest_idx
                second_digit = val

    return first_digit * 10 + second_digit


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip()
    print(sum(map(parse_line_v1, lines.split("\n"))))
    print(sum(map(parse_line_v2, lines.split("\n"))))
