# GestureFlow

GestureFlow is a hand gesture detection and system input/navigation system using Convolutional Neural Networks (CNN) with real-time detection capabilities. This project leverages TensorFlow and Keras for model training and Tkinter for creating a graphical user interface (GUI).

### Development Log

#### July 21, 2024 - Update 1

- **Real-time Hand Gesture Detection**: Detects hand gestures from live webcam feed.
- **Data Augmentation**: Enhances model training by augmenting the training data with various transformations.
- **Customizable Threshold**: Allows adjusting the detection threshold for better accuracy.
- **Simple GUI**: Provides a user-friendly interface to visualize the detection results.

*Issued by Kaustuv Bhattarai on 2024-07-21 at 13:46:45 (Sunday)*

## Installation and Setup

To install GestureFlow, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/kaustuvbhattarai/gestureflow.git
    cd gestureflow
    ```

2. Install the necessary modules:

    ```bash
    pip install tensorflow
    ```

3. Check the `adjustments.txt` file for instructions on detection sensitivity and data augmentation parameters.

4. Create a folder named dataset in the project directory with images for training. 

