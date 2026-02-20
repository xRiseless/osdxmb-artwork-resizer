#!/usr/bin/env python3
"""
OSD-XMB Artwork Resizer

This script processes ICON0.png and PIC1.png files found inside a directory tree
(starting from a given root folder, typically named "ART") and resizes them to
strict target dimensions using different strategies:

- ICON0.png → 128x128, fit with letterboxing (preserve aspect ratio, add background)
- PIC1.png  → 640x448, fill by center cropping (preserve aspect ratio, cover whole area)

The original files are overwritten. It is recommended to make a backup before running.
"""

import os
import sys
import argparse
from PIL import Image

# Target configuration per filename
TARGET_CONFIG = {
    'ICON0.png': {'size': (128, 128), 'mode': 'fit'},
    'PIC1.png':  {'size': (640, 448), 'mode': 'fill'}
}

# Supported background colors for fit mode (RGBA tuples)
BACKGROUND_COLORS = {
    'transparent': (0, 0, 0, 0),
    'black': (0, 0, 0, 255),
    'white': (255, 255, 255, 255)
}


def fit_image(img, target_size, background):
    """
    Resize image to fit inside target_size while preserving aspect ratio,
    then paste it centered onto a canvas of target_size filled with background.

    Args:
        img (PIL.Image): Input image (will be converted to RGBA).
        target_size (tuple): (width, height).
        background (tuple): RGBA color for the canvas.

    Returns:
        PIL.Image: Resulting image with exact target dimensions.
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    target_w, target_h = target_size
    img_w, img_h = img.size

    # Scale to fit inside the target rectangle
    scale = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Create background canvas
    canvas = Image.new('RGBA', target_size, background)

    # Paste centered
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.paste(resized, (x, y), resized)

    return canvas


def fill_image(img, target_size):
    """
    Resize image to completely cover target_size while preserving aspect ratio,
    then crop to the center.

    Args:
        img (PIL.Image): Input image (will be converted to RGBA).
        target_size (tuple): (width, height).

    Returns:
        PIL.Image: Resulting image with exact target dimensions.
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    target_w, target_h = target_size
    img_w, img_h = img.size

    # Scale to cover the target rectangle
    scale = max(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Crop center
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    cropped = resized.crop((left, top, right, bottom))
    return cropped


def process_file(file_path, config, background):
    """
    Open an image file, apply the appropriate transformation according to its
    configuration, and save it back (overwriting).

    Args:
        file_path (str): Path to the image file.
        config (dict): Configuration for this file type (size, mode).
        background (tuple): RGBA color used only in 'fit' mode.
    """
    try:
        with Image.open(file_path) as img:
            print(f"  Processing {os.path.basename(file_path)}: original size {img.size}")
            target_size = config['size']
            mode = config['mode']

            if mode == 'fit':
                new_img = fit_image(img, target_size, background)
            elif mode == 'fill':
                new_img = fill_image(img, target_size)
            else:
                raise ValueError(f"Unknown mode: {mode}")

            new_img.save(file_path, 'PNG')
            print(f"    -> saved as {target_size} (mode: {mode})")
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")


def process_art_folder(root_path, background):
    """
    Walk through the root directory recursively and process all ICON0.png and PIC1.png files.

    Args:
        root_path (str): Root directory to start search.
        background (tuple): RGBA background color for fit mode.
    """
    if not os.path.isdir(root_path):
        print(f"Error: '{root_path}' is not a valid directory.")
        return

    print(f"Processing artwork in: {root_path}")
    for current_dir, _, files in os.walk(root_path):
        for filename in files:
            if filename in TARGET_CONFIG:
                file_path = os.path.join(current_dir, filename)
                rel_dir = os.path.relpath(current_dir, root_path)
                print(f"\nFound {filename} in {rel_dir}")
                process_file(file_path, TARGET_CONFIG[filename], background)

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(
        description="Resize OSD-XMB artwork images (ICON0.png, PIC1.png) to strict dimensions."
    )
    parser.add_argument(
        'art_folder', nargs='?', default=None,
        help="Path to the root folder (usually named 'ART'). If omitted, looks for an 'ART' subdirectory in the current working directory."
    )
    parser.add_argument(
        '--background', '-b',
        choices=list(BACKGROUND_COLORS.keys()), default='transparent',
        help="Background color for ICON0 images (fit mode). Options: transparent (default), black, white."
    )
    args = parser.parse_args()

    # Determine the root folder
    if args.art_folder is None:
        art_folder = os.path.join(os.getcwd(), "ART")
        if not os.path.isdir(art_folder):
            print("No 'ART' folder found in current directory. Please specify a folder.")
            sys.exit(1)
    else:
        art_folder = args.art_folder

    # Get the RGBA tuple for the chosen background
    background_rgba = BACKGROUND_COLORS[args.background]

    process_art_folder(art_folder, background_rgba)


if __name__ == "__main__":
    main()