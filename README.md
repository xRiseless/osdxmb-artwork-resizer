# General:
A Python script to automatically resize **ICON0.png** and **PIC1.png** files found in OSD-XMB's artwork folder. The script ensures that images meet the required dimensions while preserving aspect ratio, using different strategies for each file type.

# Contributing:
If you want to help in developing - feel free to fork this project and customize it for your needs.

# Requirements:
- Python 3.6 or higher
- [Pillow](https://python-pillow.org/) (Python Imaging Library fork)

# How to use:
- Place the script in a convenient location.
- Run it from the command line, providing the path to the root folder that contains your artwork subdirectories (usually named ART). If you run the script without arguments, it will look for a folder named ART in the current working directory.

# Options:
- --background, -b : Set the background color for ICON0.png (fit mode). Choices: transparent (default), black, white.

# Links:
- OSD-XMB - PS2 XMB: https://github.com/HiroTex/OSD-XMB
- PS2 OSD-XMB Art Fetcher: https://github.com/laurorual/PS2-OSD-XMB-Art-Fetcher
