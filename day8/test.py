import solution
import unittest


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.lines = open("test.txt", "r").read().strip().split("\n")
        self.lines2 = open("test2.txt", "r").read().strip().split("\n")
        self.lines3 = open("test3.txt", "r").read().strip().split("\n")

    def test_part_1(self):
        values = 2, 6
        self.assertEqual(solution.part1(self.lines), values[0])
        self.assertEqual(solution.part1(self.lines2), values[1])

    def test_part_2(self):
        value = 6
        self.assertEqual(solution.part2(self.lines3), value)


if __name__ == "__main__":
    unittest.main()
