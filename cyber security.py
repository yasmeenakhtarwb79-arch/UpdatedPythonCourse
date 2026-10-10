"""A beginner-friendly terminal game that teaches cybersecurity basics."""

import random


QUESTIONS = [
	{
		"title": "Phishing email",
		"scenario": "An email says your account will be deleted today unless you click its link and sign in.",
		"options": [
			"A) Click the link immediately",
			"B) Open the service's official app or type its website address yourself",
			"C) Reply with your password",
		],
		"answer": "B",
		"tip": "Unexpected messages that create urgency may be phishing. Avoid their links and check through an official channel.",
	},
	{
		"title": "Strong passwords",
		"scenario": "Which password habit is safest?",
		"options": [
			"A) Reuse one short password everywhere",
			"B) Use a long, unique password for each account",
			"C) Use your birthday as every password",
		],
		"answer": "B",
		"tip": "Long, unique passwords help stop one stolen password from unlocking multiple accounts. A password manager can help.",
	},
	{
		"title": "Verification codes",
		"scenario": "Someone claiming to be tech support asks you to read them a sign-in verification code.",
		"options": [
			"A) Share it because they sound helpful",
			"B) Post it in a group chat",
			"C) Keep it private and contact support using its official website",
		],
		"answer": "C",
		"tip": "Verification codes are for you alone. Never share them, even with someone claiming to be support.",
	},
	{
		"title": "Software updates",
		"scenario": "Your computer offers a security update in its built-in settings. What should you do?",
		"options": [
			"A) Install it using the official update tool",
			"B) Ignore all updates permanently",
			"C) Download an update from a random pop-up ad",
		],
		"answer": "A",
		"tip": "Security updates fix known weaknesses. Install them from your device's official settings or trusted source.",
	},
	{
		"title": "Public information",
		"scenario": "You are about to post your home address and announce that you will be away all weekend.",
		"options": [
			"A) Share it publicly",
			"B) Leave out sensitive details and check the audience for your post",
			"C) Send it to strangers who ask",
		],
		"answer": "B",
		"tip": "Think before posting personal details. Online information can be copied or shared beyond its intended audience.",
	},
	{
		"title": "Unknown USB drive",
		"scenario": "You find a USB drive in a public place. It might contain useful files.",
		"options": [
			"A) Plug it into your computer to find its owner",
			"B) Give it to a trusted staff member; do not plug it in",
			"C) Use it on a friend's computer instead",
		],
		"answer": "B",
		"tip": "Unknown USB devices can contain malware. Hand them to a trusted staff member instead of connecting them to a device.",
	},
]


def play_game():
	"""Ask each question in a shuffled quiz and return the score."""
	score = 0
	questions = random.sample(QUESTIONS, len(QUESTIONS))

	for number, question in enumerate(questions, start=1):
		print(f"\n--- Challenge {number}/{len(questions)}: {question['title']} ---")
		print(question["scenario"])
		for option in question["options"]:
			print(option)

		while True:
			answer = input("Choose A, B, or C: ").strip().upper()
			if answer in ("A", "B", "C"):
				break
			print("Please enter A, B, or C.")

		if answer == question["answer"]:
			score += 1
			print("Correct! +1 point.")
		else:
			print(f"Not quite. The safest choice is {question['answer']}.")
		print(f"Cyber safety tip: {question['tip']}")

	return score


def main():
	print("=" * 48)
	print("       CYBER SAFETY: THE QUICK QUEST")
	print("=" * 48)
	print("Answer real-world scenarios, earn points, and learn safer online habits!")

	while True:
		score = play_game()
		total = len(QUESTIONS)
		print(f"\nQuest complete: {score}/{total} points.")
		if score == total:
			print("Perfect score! Excellent cyber safety skills.")
		elif score >= total // 2:
			print("Nice work! Keep practicing these safe habits.")
		else:
			print("Keep learning—the tips above are a great place to start.")

		if input("Play again? (y/n): ").strip().lower() not in ("y", "yes"):
			print("Thanks for playing. Stay curious and stay safe online!")
			break


if __name__ == "__main__":
	main()
