"""Control the mouse pointer with hand gestures from a webcam.

Install dependencies: pip install opencv-python mediapipe pyautogui
Move your index finger to move the pointer. Pinch your thumb and index finger
to click. Press Q in the video window to quit.
"""

import cv2
import mediapipe as mp
import pyautogui


def main():
	pyautogui.FAILSAFE = True  # Move the pointer to a screen corner to stop it.
	screen_width, screen_height = pyautogui.size()
	camera = cv2.VideoCapture(0)
	if not camera.isOpened():
		raise RuntimeError("Unable to access the webcam.")

	hands_module = mp.solutions.hands
	smooth_x, smooth_y = screen_width // 2, screen_height // 2
	pinch_was_active = False

	try:
		with hands_module.Hands(
			max_num_hands=1,
			min_detection_confidence=0.7,
			min_tracking_confidence=0.6,
		) as hands:
			while True:
				ok, frame = camera.read()
				if not ok:
					break

				frame = cv2.flip(frame, 1)
				frame_height, frame_width = frame.shape[:2]
				rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				result = hands.process(rgb)

				if result.multi_hand_landmarks:
					points = result.multi_hand_landmarks[0].landmark
					index_tip, thumb_tip = points[8], points[4]

					# Map the central 80% of the camera view to the screen.
					target_x = int((index_tip.x - 0.1) * screen_width / 0.8)
					target_y = int((index_tip.y - 0.1) * screen_height / 0.8)
					target_x = max(0, min(screen_width - 1, target_x))
					target_y = max(0, min(screen_height - 1, target_y))
					smooth_x += (target_x - smooth_x) / 5
					smooth_y += (target_y - smooth_y) / 5
					pyautogui.moveTo(int(smooth_x), int(smooth_y))

					distance = ((index_tip.x - thumb_tip.x) ** 2 +
								(index_tip.y - thumb_tip.y) ** 2) ** 0.5
					pinching = distance < 0.045
					if pinching and not pinch_was_active:
						pyautogui.click()
					pinch_was_active = pinching

					cx, cy = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
					cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
					cv2.putText(frame, "Pinch to click | Q to quit", (10, 30),
								cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
				else:
					pinch_was_active = False

				cv2.imshow("Hand Gesture Controller", frame)
				if cv2.waitKey(1) & 0xFF == ord("q"):
					break
	finally:
		camera.release()
		cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
