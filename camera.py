import cv2 as cv
import os
import time

# Open the webcam
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a directory to save photos
os.makedirs("photos", exist_ok=True)
print("Taking photos... Press '1' to capture and 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Display the webcam feed
    cv.imshow('Webcam', frame)

    # Wait for keypress
    key = cv.waitKey(1) & 0xFF

    # If '1' is pressed, capture and save the photo
    if key == ord('1'):
        img_name = f"photos/photo_{int(time.time())}.jpg"
        cv.imwrite(img_name, frame)
        print(f"Saved {img_name}")

    # If 'q' is pressed, exit the loop
    elif key == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv.destroyAllWindows()
