"""
簡單的 Wordle-like CLI 遊戲 (中文說明)

使用說明:
  - 這是一個 5 字母的 Wordle 類遊戲，玩家有 6 次猜測機會。
  - 每次猜測會顯示每個字母的回饋：綠色(正確位置)、黃色(存在於單字但位置錯誤)、灰色(不存在)
  - 可重複遊玩。

程式包含函式:
  - check_guess(secret, guess) -> list of 'G'|'Y'|'_'
  - format_feedback(guess, feedback, use_color=True) -> human-readable string
  - main() -> CLI 入口

作者: 自動生成示例
"""

import random
import sys
from typing import List

# 小型內建 5-letter 單字表（可擴充）
WORD_LIST = [
	"apple", "banal", "candy", "delta", "eagle", "flame", "grape", "house",
	"irony", "joker", "knock", "lemon", "mango", "naval", "ocean", "party",
	"quart", "river", "sugar", "tiger", "urban", "vivid", "whale", "xenon",
	"young", "zesty"
]


def check_guess(secret: str, guess: str) -> List[str]:
	"""返回每個字母的回饋列表：'G' = correct (綠), 'Y' = present wrong place (黃), '_' = absent (灰)

	以 Wordle 規則處理重複字母：先標記綠色，然後根據尚未被標記的 secret 字母計算黃色。
	"""
	secret = secret.lower()
	guess = guess.lower()
	if len(secret) != len(guess):
		raise ValueError("secret and guess must have the same length")

	n = len(secret)
	feedback = ["_"] * n
	secret_used = [False] * n

	# 先標記綠色
	for i in range(n):
		if guess[i] == secret[i]:
			feedback[i] = "G"
			secret_used[i] = True

	# 標記黃色或灰色
	for i in range(n):
		if feedback[i] == "G":
			continue
		found = False
		for j in range(n):
			if not secret_used[j] and guess[i] == secret[j]:
				found = True
				secret_used[j] = True
				break
		feedback[i] = "Y" if found else "_"

	return feedback


def format_feedback(guess: str, feedback: List[str], use_color: bool = True) -> str:
	"""把回饋格式化為可讀字串，預設使用 ANSI 顏色（若終端支援）。

	例如：guess='apple', feedback=['G','_','Y','_','G']
	輸出：綠色 a, 灰色 p, 黃色 p, ...
	"""
	parts = []
	for ch, f in zip(guess, feedback):
		if not use_color:
			parts.append(f"{ch.upper()}({f})")
			continue

		if f == "G":
			# 綠底白字
			parts.append(f"\x1b[30;42m {ch.upper()} \x1b[0m")
		elif f == "Y":
			# 黃底黑字
			parts.append(f"\x1b[30;43m {ch.upper()} \x1b[0m")
		else:
			# 灰色/預設
			parts.append(f"\x1b[30;47m {ch.upper()} \x1b[0m")
	return " ".join(parts)


def choose_secret(word_list=WORD_LIST) -> str:
	return random.choice(word_list)


def is_valid_guess(guess: str, length: int = 5) -> bool:
	return len(guess) == length and guess.isalpha()


def main():
	"""簡單的 CLI 遊戲循環"""
	print("歡迎來到簡單 Wordle CLI！(5-letter, 6 次機會)")

	while True:
		secret = choose_secret()
		attempts = 6
		won = False

		# 遊戲回合
		for turn in range(1, attempts + 1):
			while True:
				try:
					guess = input(f"第 {turn} 次猜測，請輸入 5 個字母：").strip()
				except (EOFError, KeyboardInterrupt):
					print("\n遊戲中止。")
					sys.exit(0)

				if not is_valid_guess(guess):
					print("無效輸入，請輸入 5 個英文字母，例：apple")
					continue
				break

			feedback = check_guess(secret, guess)
			print(format_feedback(guess, feedback, use_color=True))

			if all(f == "G" for f in feedback):
				print(f"恭喜，你猜對了！答案是 {secret.upper()}，共用 {turn} 次。")
				won = True
				break

		if not won:
			print(f"很遺憾，答案是 {secret.upper()}。")

		again = input("要再玩一次嗎？(y/n): ").strip().lower()
		if again not in ("y", "yes"):
			print("謝謝遊玩！")
			break


if __name__ == "__main__":
	main()

