# Image to ASCII Converter

## Table of contents
* [Overview](#overview)
* [Technologies](#technologies)
* [Setup](#setup)

## Overview
This program takes images from the *./imgs/* folder and makes then into coloured ascii text drawings.  
There are photos that are already in the *./imgs/* folder and you can choose from these default photos; however, you can also add your own photos to the folder and the newly-added photo can be selected in the program.


## Technologies
- **Python 3.8**
- **Pillow 6.2**
  - for image minipulation
- **glob**
  - for getting images from a folder
- **Ansi Escape Sequences**
  - for converting *RGB* colour to colour representable in terminals
  - generating these sequences from *RGB* is my own algorithm and allows the requirements to be limited to only **Pillow**

## Setup
To run this project, install the requirements and then run the program:

    pip3 install -r requirements
    python convert.py

## Limitations
- The program can only run **png** and **jpg** *(PNG, JPG, jpeg...)* files
  - This means that video and gifs are not supported
