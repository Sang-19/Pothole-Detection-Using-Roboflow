import cv2 as cv
import os
import time
from roboflow import Roboflow
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np

# Define the directory to save the image
save_dir = os.getcwd()  # Save in the same directory as the script

# Open the webcam
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Taking photos... Press '1' to capture and 'q' to quit.")

# Create a matplotlib figure for displaying the webcam feed
fig, ax = plt.subplots()
plt.ion()  # Turn on interactive mode
canvas = fig.canvas

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert the frame to RGB (matplotlib expects RGB images)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    # Clear the previous image
    ax.clear()
    ax.imshow(rgb_frame)
    ax.set_title('Webcam Feed')
    ax.axis('off')
    
    # Draw the new frame
    canvas.draw()
    
    # Check for keypresses
    if plt.waitforbuttonpress(0.1):
        key = plt.gcf().canvas.manager.key_press_event.key
        
        if key == '1':
            img_name = os.path.join(save_dir, "captured_image.jpg")
            cv.imwrite(img_name, frame)
            print(f"Captured and saved {img_name}")
            break
        elif key == 'q':
            print("Exiting...")
            break

# Release the webcam and close the plot
cap.release()
plt.close('all')

# Run the Roboflow model prediction
rf = Roboflow(api_key="y7q17Kl4AJHZMjoSDn58")
project = rf.workspace("pothole-detectionn").project("pothole-detection-rk9fr")
model = project.version(1).model

prediction = model.predict(img_name, confidence=1, overlap=30)

# Open the captured image for drawing
img = Image.open(img_name)
draw = ImageDraw.Draw(img)

# Get predictions and draw rectangles
predictions = prediction.json()['predictions']
rectangle_color = (255, 0, 0)
rectangle_width = 2

for pred in predictions:
    x0 = pred['x'] - pred['width'] / 2
    y0 = pred['y'] - pred['height'] / 2
    x1 = pred['x'] + pred['width'] / 2
    y1 = pred['y'] + pred['height'] / 2
    draw.rectangle([x0, y0, x1, y1], outline=rectangle_color, width=rectangle_width)

# Save and show the result
output_img_path = os.path.join(save_dir, "pothole_output.jpg")
img.save(output_img_path)
plt.imshow(img)
plt.axis('off')
plt.show()
