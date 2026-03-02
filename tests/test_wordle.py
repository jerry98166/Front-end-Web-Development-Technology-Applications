import unittest
from pathlib import Path
import importlib.util
import sys

# 透過 importlib 從檔案載入 module，因為檔名以數字開頭不能直接作為模組名稱匯入
module_path = Path(__file__).resolve().parents[1] / "1015.py"
spec = importlib.util.spec_from_file_location("wordle1015", str(module_path))
wordle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wordle)
check_guess = wordle.check_guess


class TestCheckGuess(unittest.TestCase):
    def test_all_green(self):
        self.assertEqual(check_guess('apple', 'apple'), ['G', 'G', 'G', 'G', 'G'])

    def test_all_absent(self):
        self.assertEqual(check_guess('apple', 'ttttt'), ['_', '_', '_', '_', '_'])

    def test_mixed(self):
        # secret: 'apple', guess: 'apply' -> last letter differs
        self.assertEqual(check_guess('apple', 'apply'), ['G', 'G', 'G', 'G', '_'])

    def test_yellow(self):
        # 'peach' shares p,e,a with 'apple'
        self.assertEqual(check_guess('apple', 'peach'), ['Y', 'Y', 'Y', '_', '_'])

    def test_repeated_letters_secret(self):
        # secret has two p's, guess has three p's -> only two can be matched
        self.assertEqual(check_guess('apple', 'ppppp'), ['_', 'G', 'G', '_', '_'])


if __name__ == '__main__':
    unittest.main()
