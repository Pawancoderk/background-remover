import cv2
import numpy as np
from PIL import Image
import sys


def remove_background(input_path, output_path, lower_color, upper_color):
    # Read image
    image = cv2.imread(input_path)
    if image is None:
        print(f"Could not read input image: {input_path}")
        return

    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create mask based on color range
    lower = np.array(lower_color, dtype=np.uint8)
    upper = np.array(upper_color, dtype=np.uint8)
    mask = cv2.inRange(image_rgb, lower, upper)

    # Invert mask to get foreground
    mask_inv = cv2.bitwise_not(mask)

    # Convert mask to 3 channels
    mask_inv_3ch = cv2.merge([mask_inv, mask_inv, mask_inv])
    fg = cv2.bitwise_and(image_rgb, mask_inv_3ch)

    # Convert to RGBA
    rgba = cv2.cvtColor(fg, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask_inv

    # Save with transparency using PIL
    result = Image.fromarray(rgba)
    result.save(output_path)
    print(f"Saved output image with transparent background: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python remove_bg.py <input_image> <output_image> [lower_R lower_G lower_B upper_R upper_G upper_B]")
        print("Example for white background: python remove_bg.py input.jpg output.png 200 200 200 255 255 255")
        return
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if len(sys.argv) == 9:
        lower_color = [int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])]
        upper_color = [int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])]
    else:
        # Default: white background
        lower_color = [200, 200, 200]
        upper_color = [255, 255, 255]
    remove_background(input_path, output_path, lower_color, upper_color)


if __name__ == "__main__":
    main()
