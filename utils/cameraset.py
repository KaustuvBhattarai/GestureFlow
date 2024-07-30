import cv2
import os

def capture_images(save_directory, image_prefix="image", num_images=10): #increase number of images if you want more
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Images")

    img_counter = 0
    while img_counter < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        cv2.imshow("Capture Images", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = os.path.join(save_directory, f"{image_prefix}_{img_counter}.png")
            cv2.imwrite(img_name, frame)
            print(f"{img_name} saved!")
            img_counter += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    save_directory = r"U:\testingcnn\dataset\no_hand"  # Use raw string 
    capture_images(save_directory)
