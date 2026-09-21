"""Safe, beginner-friendly cybersecurity learning toolkit.

Run this file to practice password hygiene and basic defensive concepts.
"""

import getpass
import math
import string


def password_strength(password: str) -> tuple[int, str]:
	"""Return a simple score and recommendation for a password."""
	score = 0
	checks = (
		len(password) >= 12,
		any(char.islower() for char in password),
		any(char.isupper() for char in password),
		any(char.isdigit() for char in password),
		any(char in string.punctuation for char in password),
	)
	score = sum(checks)

	if len(set(password)) < max(4, len(password) // 3):
		score = max(0, score - 1)

	labels = {
		0: "Very weak",
		1: "Weak",
		2: "Fair",
		3: "Good",
		4: "Strong",
		5: "Very strong",
	}
	return score, labels[score]


def estimate_entropy(password: str) -> float:
	"""Estimate password entropy; this is educational, not a crack-time test."""
	alphabet = 0
	if any(c.islower() for c in password):
		alphabet += 26
	if any(c.isupper() for c in password):
		alphabet += 26
	if any(c.isdigit() for c in password):
		alphabet += 10
	if any(c in string.punctuation for c in password):
		alphabet += len(string.punctuation)
	return len(password) * math.log2(alphabet) if alphabet else 0.0


def main() -> None:
	print("Cybersecurity learning: password hygiene")
	print("Use a unique password or passphrase for every account.\n")
	password = getpass.getpass("Enter a sample password (not a real one): ")
	score, label = password_strength(password)
	print(f"\nRating: {label} ({score}/5)")
	print(f"Estimated entropy: {estimate_entropy(password):.1f} bits")
	if score < 4:
		print("Tip: use 12+ characters with mixed character types, or a long passphrase.")
	else:
		print("Good start: also enable MFA and use a password manager.")
	print("Never share passwords or test systems without explicit permission.")


if __name__ == "__main__":
	main()
