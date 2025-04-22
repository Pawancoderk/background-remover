# Image Background Remover

This Python application removes the background from an image (with a solid color) and outputs a PNG with a transparent background.

## Requirements
- Python 3.7+
- opencv-python
- numpy
- Pillow

Install dependencies:
```
pip install -r requirements.txt
```

## Usage
```
python remove_bg.py <input_image> <output_image> [lower_R lower_G lower_B upper_R upper_G upper_B]
```
- `input_image`: Path to the input image file.
- `output_image`: Path to save the output PNG image.
- `[lower_R lower_G lower_B upper_R upper_G upper_B]`: (Optional) RGB color range for background. Default is white background.

### Example
Remove white background:
```
python remove_bg.py input.jpg output.png 200 200 200 255 255 255
```

## Notes
- Works best with images that have a solid color background.
- For complex backgrounds, advanced methods like GrabCut may be required.
