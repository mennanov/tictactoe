import unittest

import finder


class FinderTest(unittest.TestCase):
    def testRaisesExceptionForInvalidInput(self):
        invalid_fields = (
            [],
            [[]],
            [['x', 'x', 'x'], ['0', '0', '0'], ['x', 'x']],
        )
        for field in invalid_fields:
            with self.assertRaises(ValueError):
                finder.find_in_frame(field)

    def testHorizontalCases(self):
        fields = (
            [
                ['x', 'x', 'x'],
                ['0', '0', 'x'],
                ['x', '0', '0']
            ],
            [
                ['0', '0', 'x'],
                ['x', 'x', 'x'],
                ['x', '0', '0']
            ],
            [
                ['0', '0', 'x'],
                ['x', 'x', '0'],
                ['0', '0', '0'],
            ]
        )
        for field in fields:
            self.assertTrue(finder.find_in_frame(field))

    def testVerticalCases(self):
        fields = (
            [
                ['x', 'x', '0'],
                ['x', 'x', '0'],
                ['x', '0', 'x']
            ],
            [
                ['0', '0', 'x'],
                ['x', '0', 'x'],
                ['x', '0', '0']
            ],
            [
                ['0', 'x', '0'],
                ['x', 'x', '0'],
                ['0', '0', '0'],
            ]
        )
        for field in fields:
            self.assertTrue(finder.find_in_frame(field))

    def testDiagonalCases(self):
        fields = (
            [
                ['x', 'x', '0'],
                ['0', 'x', '0'],
                ['x', '0', 'x']
            ],
            [
                ['0', '0', 'x'],
                ['x', 'x', '0'],
                ['x', '0', '0']
            ],
            [
                ['x', 'x', '0'],
                ['x', '0', '0'],
                ['0', '0', '0'],
            ],
            [
                ['0', 'x', '0'],
                ['x', '0', 'x'],
                ['x', '0', '0'],
            ]
        )
        for field in fields:
            self.assertTrue(finder.find_in_frame(field))

    def testNoWinningCases(self):
        fields = (
            [
                ['x', 'x', '0'],
                ['0', 'x', 'x'],
                ['x', '0', '0']
            ],
            [
                ['0', '0', 'x'],
                ['x', 'x', '0'],
                ['0', 'x', '0']
            ],
            [
                ['x', 'x', '0'],
                ['0', '0', 'x'],
                ['x', '0', 'x'],
            ],
            [
                ['0', 'x', '0'],
                ['x', '0', 'x'],
                ['x', '0', 'x'],
            ]
        )
        for field in fields:
            self.assertFalse(finder.find_in_frame(field), field)


if __name__ == '__main__':
    unittest.main()
