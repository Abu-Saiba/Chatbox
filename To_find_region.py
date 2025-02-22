#To Find Correct Region Coordinates:
import pyautogui
print("Move mouse to top-left of chat area and press Ctrl+C")
x1, y1 = pyautogui.position()
print("Move mouse to bottom-right and press Ctrl+C")
x2, y2 = pyautogui.position()
print(f"Region: ({x1}, {y1}, {x2}, {y2})")