from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

def initialize_model():
    """Initialize Roboflow model"""
    print("Initializing Roboflow model...")
    rf = Roboflow(api_key="y7q17Kl4AJHZMjoSDn58")
    project = rf.workspace("pothole-detectionn").project("pothole-detection-rk9fr")
    model = project.version(1).model
    return model

def process_image_with_confidence(model, image_path, confidence_threshold=40, overlap_threshold=50):
    """Process single image with adjustable confidence threshold"""
    print(f"\nProcessing {image_path}")
    print(f"Confidence threshold: {confidence_threshold}%")
    print(f"Overlap threshold: {overlap_threshold}%")
    
    # Run prediction with adjusted parameters
    prediction = model.predict(image_path, confidence=confidence_threshold, overlap=overlap_threshold)
    
    # Open image for drawing
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Get predictions
    predictions = prediction.json().get('predictions', [])
    print(f"Found {len(predictions)} potential potholes")
    
    # Draw rectangles for each detection
    rectangle_color = (255, 0, 0)  # Red
    rectangle_width = 3
    
    print(f"\nRaw prediction values for {image_path}:")
    print(predictions)  # Debug output
    
    for i, pred in enumerate(predictions):
        confidence = pred.get('confidence', 0)
        class_name = pred.get('class', 'pothole')
        
        print(f"\n  Detection {i+1}: {class_name} (confidence: {confidence:.2%})")
        print(f"  Raw values: x={pred.get('x')}, y={pred.get('y')}, width={pred.get('width')}, height={pred.get('height')}")
        
        # Get image dimensions
        img_width, img_height = img.size
        
        # Check if coordinates are normalized (values between 0 and 1)
        if pred['x'] <= 1.0 and pred['y'] <= 1.0 and pred['width'] <= 1.0 and pred['height'] <= 1.0:
            # Convert normalized coordinates to pixel coordinates
            x_center = pred['x'] * img_width
            y_center = pred['y'] * img_height
            width = pred['width'] * img_width
            height = pred['height'] * img_height
        else:
            # Use coordinates as they are (already in pixels)
            x_center = pred['x']
            y_center = pred['y']
            width = pred['width']
            height = pred['height']
        
        # Calculate bounding box coordinates
        x0 = x_center - width / 2
        y0 = y_center - height / 2
        x1 = x_center + width / 2
        y1 = y_center + height / 2
        
        # Draw rectangle
        draw.rectangle([x0, y0, x1, y1], outline=rectangle_color, width=rectangle_width)
        
        # Add confidence label
        label = f"{class_name}: {confidence:.1%}"
        try:
            # Try to use a font, fallback to default if not available
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        draw.text((x0, y0-20), label, fill=rectangle_color, font=font)
    
    return img, predictions

def test_different_confidence_levels(model, image_path):
    """Test different confidence levels to find optimal settings"""
    confidence_levels = [10, 20, 30, 40, 50, 60, 70]
    
    print(f"\n=== Testing different confidence levels for {image_path} ===")
    
    best_confidence = None
    best_count = 0
    
    for confidence in confidence_levels:
        prediction = model.predict(image_path, confidence=confidence, overlap=50)
        predictions = prediction.json().get('predictions', [])
        print(f"Confidence {confidence}%: {len(predictions)} detections")
        
        # Store the confidence level that gives reasonable number of detections (1-5)
        if 1 <= len(predictions) <= 5 and len(predictions) > best_count:
            best_confidence = confidence
            best_count = len(predictions)
    
    return best_confidence or 40  # Default to 40% if no good confidence found

def main():
    """Main function"""
    model = initialize_model()

    # Open a file dialog for the user to select image files
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    image_files = filedialog.askopenfilenames(
        title="Select image files for pothole detection",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    image_files = list(image_files)  # Convert from tuple to list

    if not image_files:
        print("No image files selected.")
        return

    for image_file in image_files:
        if os.path.exists(image_file):
            # Test different confidence levels to find optimal
            optimal_confidence = test_different_confidence_levels(model, image_file)
            print(f"Using optimal confidence: {optimal_confidence}%")
            
            # Process with optimal confidence
            processed_img, predictions = process_image_with_confidence(
                model, image_file, confidence_threshold=optimal_confidence
            )
            
            # Save result
            output_name = f"improved_{os.path.basename(image_file)}"
            processed_img.save(output_name)
            print(f"Saved improved result: {output_name}")
            
            # Display original and processed side by side
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Original image
            original_img = Image.open(image_file)
            ax1.imshow(original_img)
            ax1.set_title(f"Original: {os.path.basename(image_file)}")
            ax1.axis('off')
            
            # Processed image
            ax2.imshow(processed_img)
            ax2.set_title(f"Detected Potholes ({len(predictions)} found)")
            ax2.axis('off')
            
            plt.tight_layout()
            plt.show()
        else:
            print(f"Image {image_file} not found")

if __name__ == "__main__":
    main()
