from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def remove_background(image_stream, lower_color, upper_color):
    # Read image from stream
    image = Image.open(image_stream).convert('RGB')
    image_np = np.array(image)
    # Create mask based on color range
    lower = np.array(lower_color, dtype=np.uint8)
    upper = np.array(upper_color, dtype=np.uint8)
    mask = cv2.inRange(image_np, lower, upper)
    mask_inv = cv2.bitwise_not(mask)
    mask_inv_3ch = cv2.merge([mask_inv, mask_inv, mask_inv])
    fg = cv2.bitwise_and(image_np, mask_inv_3ch)
    rgba = cv2.cvtColor(fg, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask_inv
    result = Image.fromarray(rgba)
    return result

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        # Get color range from form or use default
        try:
            lower = [int(request.form.get('lower_r', 200)), int(request.form.get('lower_g', 200)), int(request.form.get('lower_b', 200))]
            upper = [int(request.form.get('upper_r', 255)), int(request.form.get('upper_g', 255)), int(request.form.get('upper_b', 255))]
        except Exception:
            lower = [200, 200, 200]
            upper = [255, 255, 255]
        result_img = remove_background(file.stream, lower, upper)
        img_io = BytesIO()
        result_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
