import solution
import unittest


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.lines = open("test.txt", "r").read().strip().split("\n")

    def test_part_1(self):
        values = 374
        self.assertEqual(solution.part1(self.lines), values)

    def test_part_2(self):
        multipliers = 10, 100
        values = 1030, 8410
        self.assertEqual(solution.part2(self.lines, multipliers[0]), values[0])
        self.assertEqual(solution.part2(self.lines, multipliers[1]), values[1])


if __name__ == "__main__":
    unittest.main()
