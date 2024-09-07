from roboflow import Roboflow
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

rf = Roboflow(api_key="y7q17Kl4AJHZMjoSDn58")
project = rf.workspace("pothole-detectionn").project("pothole-detection-rk9fr")
model = project.version(1).model

prediction = model.predict("image2.png", confidence=1, overlap=30)

img = Image.open("image2.png")
draw = ImageDraw.Draw(img)

predictions = prediction.json()['predictions']

rectangle_color = (255, 0 , 0) 
rectangle_width = 2

for pred in predictions:
    x0 = pred['x'] - pred['width'] / 2
    y0 = pred['y'] - pred['height'] / 2
    x1 = pred['x'] + pred['width'] / 2
    y1 = pred['y'] + pred['height'] / 2
    draw.rectangle([x0, y0, x1, y1], outline=rectangle_color, width=rectangle_width)

img.save("pothole_output.jpg")
plt.imshow(img)
plt.axis('off') 
plt.show()
