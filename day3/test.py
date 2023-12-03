import solution

if __name__ == "__main__":
    lines = open("test.txt", "r").read().strip().split("\n")

    part_1_result = solution.sum_parts(lines)
    expected_result_1 = 4361
    assert (
        part_1_result == 4361
    ), f"Expected {expected_result_1} but got {part_1_result}"

    part_2_result = solution.sum_gears(lines)
    expected_result_2 = 467835
    assert (
        part_2_result == expected_result_2
    ), f"Expected {expected_result_2} but got {part_2_result}"

    print("All tests passed")
