import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Mediapipe initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Function to detect hands
def detect_hands(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return image

# Function to update frame in GUI
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = detect_hands(frame)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, update_frame)

# Initialize the GUI window
root = tk.Tk()
root.title("Hand Detection")
lmain = Label(root)
lmain.pack()

# Start capturing video
cap = cv2.VideoCapture(0)

# Start the GUI
update_frame()
root.mainloop()

# Release the video capture when GUI is closed
cap.release()
cv2.destroyAllWindows()
