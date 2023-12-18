import solution
import unittest


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.lines = open("test.txt", "r").read().strip().split("\n")

    def test_part_1(self):
        values = 136
        self.assertEqual(solution.part1(self.lines), values)

    def test_part_2(self):
        value = 64
        self.assertEqual(solution.part2(self.lines), value)


if __name__ == "__main__":
    unittest.main()
