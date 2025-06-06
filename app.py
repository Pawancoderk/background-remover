from flask import Flask, render_template, request, send_file, redirect, url_for
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def remove_background_rembg(image_stream):
    input_image = Image.open(image_stream)
    # Resize if too large
    max_size = 720
    if max(input_image.size) > max_size:
        input_image.thumbnail((max_size, max_size))
    output_image = remove(input_image)
    return output_image



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        result_img = remove_background_rembg(file.stream)
        img_io = BytesIO()
        result_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    return render_template('index.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
