from flask import Flask, request, send_file, render_template
import cv2
import numpy as np
import random
import os

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file uploaded", 400

    # Save the uploaded file
    file = request.files['file']
    input_path = 'input_image.jpg'
    file.save(input_path)

    # Load the uploaded image
    new_area_image = cv2.imread(input_path)
    if new_area_image is None:
        return "Invalid image", 400

    # Convert the image to HSV color space to better isolate the green lines
    hsv_image = cv2.cvtColor(new_area_image, cv2.COLOR_BGR2HSV)

    # Define HSV range for green color
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Create a mask that isolates the green lines
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Dilate the green lines mask
    kernel_green = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated_green_lines = cv2.dilate(green_mask, kernel_green, iterations=2)

    # Find contours based on the green lines mask
    contours_green_divisions, _ = cv2.findContours(cv2.bitwise_not(dilated_green_lines), 
                                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an overlay to fill each detected area with a unique color
    overlay_colored_areas = new_area_image.copy()
    for contour in contours_green_divisions:
        color_area = [random.randint(0, 255) for _ in range(3)]
        cv2.drawContours(overlay_colored_areas, [contour], -1, color_area, thickness=cv2.FILLED)

    # Blend the overlay with the original image
    output_colored_areas = cv2.addWeighted(overlay_colored_areas, 0.4, new_area_image, 0.6, 0)
    output_path = 'output_image.jpg'
    cv2.imwrite(output_path, output_colored_areas)

    # Send the processed image as a response
    return send_file(output_path, mimetype='image/jpeg', as_attachment=True, download_name="processed_image.jpg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
