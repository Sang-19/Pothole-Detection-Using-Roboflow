from roboflow import Roboflow
from PIL import Image
import matplotlib.pyplot as plt

rf = Roboflow(api_key="y7q17Kl4AJHZMjoSDn58")
## project = rf.workspace("pothole-detectionn").project("pothole-detection-rk9fr")
project = rf.workspace("pothole-2d8gl").project("pothole__detection")
model = project.version(1).model
## model = project.version(1).model

prediction = model.predict("image0.png", confidence=1, overlap=30)
prediction.save("pothole_output.jpg")

img = Image.open("pothole_output.jpg")
plt.imshow(img)
plt.axis('off')  
plt.show()

