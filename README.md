GestureFlow
GestureFlow is a hand gesture detection system using Convolutional Neural Networks (CNN) with real-time detection capabilities. This project leverages tensorflow and keras for model training and tkinter for creating a graphical user interface (GUI). The primary objective of GestureFlow is to detect and classify hand gestures from images and live video streams.

Features
Real-time Hand Gesture Detection: Detects hand gestures from live webcam feed.
Data Augmentation: Enhances model training by augmenting the training data with various transformations.
Customizable Threshold: Allows adjusting the detection threshold for better accuracy.
Simple GUI: Provides a user-friendly interface to visualize the detection results.
Installation
To get started with GestureFlow, you need to clone the repository and install the required dependencies:

bash
Copy code
git clone https://github.com/kaustuvbhattarai/gestureflow.git
cd gestureflow
pip install -r requirements.txt
Dataset Preparation
Prepare your dataset with the following directory structure:

markdown
Copy code
hands/
    hand/
        hand1.jpg
        hand2.jpg
        ...
    no_hand/
        no_hand1.jpg
        no_hand2.jpg
        ...
Place your dataset in the hands folder within the project directory.

Training the Model
To train the model, run the following script:

bash
Copy code
python train.py
This will train a CNN model on your dataset and save the trained model as hand_detection_model.h5.

Running the GUI for Real-Time Detection
To start the real-time hand gesture detection GUI, run:

bash
Copy code
python gui.py
This will launch a tkinter window displaying the live webcam feed with hand detection results.

Customization
Adjusting Detection Threshold
You can adjust the detection threshold in the detect_hand_in_image function in gui.py to make the detection more or less sensitive:

python
Copy code
def detect_hand_in_image(model, image, threshold=0.4):
    # Function implementation
Data Augmentation
Data augmentation parameters can be modified in train.py to improve the robustness of the model:

python
Copy code
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)
Dependencies
TensorFlow
Keras
OpenCV
Pillow
Tkinter
Install all dependencies using the provided requirements.txt file:

bash
Copy code
pip install -r requirements.txt
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or new features.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Special thanks to the developers of TensorFlow, Keras, OpenCV, and Tkinter for their excellent libraries.

