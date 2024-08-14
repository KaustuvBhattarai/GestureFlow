Functionality archives: 

-----------------------------------------------------------------------------------------------------------------

1. control_cursor(index_finger_tip, width, height)
This function takes the position of the index finger tip as input and moves the cursor on the screen accordingly.
Parameters:
index_finger_tip: Tuple containing the x and y coordinates of the index finger tip.
width: The width of the screen (used to map the coordinates).
height: The height of the screen (used to map the coordinates).
The function calculates the new position for the cursor by mapping the hand coordinates to the screen dimensions.
It uses pyautogui.moveTo(x, y) to move the cursor to the calculated position.

2. click_event()
This function simulates a mouse click when a specific gesture is detected (like closing the hand to form a fist).
The function checks if the hand gesture meets the criteria for a click event (e.g., detecting a fist).
If the criteria are met, it uses pyautogui.click() to simulate a mouse click at the current cursor position.

3. toggle_mouse_control()
This function is linked to a button in the GUI that enables or disables gesture-based mouse control.
When the button is clicked, the function toggles a boolean flag that determines whether mouse control is active.
If enabled, the cursor movements and click events are controlled by hand gestures; otherwise, they are disabled.


-----------------------------------------------------------------------------------------------------------------

Logging with Timestamps
The application includes a logging feature that records each session's activity in a text file. The log files are stored with a date and timestamp in the filename, making it easy to track and analyze previous sessions.

1. log_session_data()
This function creates and writes logs of the current session into a text file.

How it Works:
Upon each run of the application, a new log file is created with a filename containing the current date and timestamp.
The log file records key events, such as when mouse control is toggled, theme changes, and any errors encountered during the session.
Example Code:
python
Copy code
import datetime

def log_session_data(log_message):
    # Create a log file with the current date and timestamp in the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log_{timestamp}.txt"
    
    # Open the log file and write the log message
    with open(log_filename, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {log_message}\n")

Parameters:
log_message: The message or event details to be logged in the file.
File Location:
The log files are stored in the same directory as the application. You can modify the path to save logs in a specific folder.
2. on_closing()
This function is triggered when the user attempts to close the application window.
Before closing the application, the function logs the event by calling log_session_data() with a message indicating that the application is closing.
It then safely terminates the application, ensuring that all resources are released properly.

-----------------------------------------------------------------------------------------------------------------

Issued on Aug 14,2024
