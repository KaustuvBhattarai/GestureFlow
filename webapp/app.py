from flask import Flask, render_template, Response
import cv2
import os
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Load the model
current_dir = os.path.dirname(os.path.abspath(__file__))
model = tf.keras.models.load_model(os.path.join(current_dir, "hand_detection_model.h5"))

def detect_hand_in_image(image):
    try:
        image_resized = cv2.resize(image, (64, 64))
        image_array = np.expand_dims(image_resized, axis=0) / 255.0
        prediction = model.predict(image_array)
        return "Hand" if prediction[0][0] > 0.5 else "No Hand"
    except Exception as e:
        print(f"Error in detect_hand_in_image: {e}")
        return "No Hand"

def gen_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break
        else:
            result = detect_hand_in_image(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
