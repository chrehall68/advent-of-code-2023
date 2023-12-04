import solution

if __name__ == "__main__":
    lines = open("test.txt", "r").read().strip().split("\n")

    part_1_result = sum(map(solution.get_line_worth, lines))
    expected_result_1 = 13
    assert (
        part_1_result == expected_result_1
    ), f"Expected {expected_result_1} but got {part_1_result}"

    part_2_result = solution.get_copied_count(lines)
    expected_result_2 = 30
    assert (
        part_2_result == expected_result_2
    ), f"Expected {expected_result_2} but got {part_2_result}"

    print("All tests passed")
