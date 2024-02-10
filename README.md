# Image Processing Tools


## Overview
This program does interesting things with a picture. Here's what it does, step by step:

1. **Slicing into strips:** The program divides the original picture into many thin vertical strips of the same width.

2. **Selecting strips:** Then, it selects all the strips with odd numbers (first, third, fifth, etc.) and sticks them together, keeping their initial order. This creates a new image where objects seem stretched vertically. The same is done with the even strips, resulting in a second similar image.

3. **Joining images:** The two obtained images are then joined horizontally, placing the second one to the right of the first. The size of the final image matches that of the original picture.

4. **Working with horizontal strips:** Next, the program repeats the whole process but with horizontal strips. It divides the new double image into horizontal strips, processes them in the same way as the vertical ones, and creates a third image. This one will have four small copies of the original picture, reduced to a quarter of their size.

5. **Final image:** In the end, the program places all three stages of processed pictures (the original, with two vertically stretched images, and with four reduced copies) on one large image, arranging them vertically one below the other for clarity.

Note: The thinner the strips the program slices the picture into, the clearer and higher quality the four small images on the final stage will appear.


## Requirements
- Python 3.8+ (compatibility with other Python versions is not guaranteed).
- Required libraries:
  ```
  numpy
  PIL (Pillow)
  yaml
  ```
  To install all libraries at once, run the command: `pip install -r requirements.txt`.


## Installation
1. Ensure Python 3.8+ is installed on your system.
2. Clone this repository or download the project files to your computer:
   ```
   git clone https://github.com/Ceslavas/image_processing_tools.git "D:\your_folder"
   ```


## Configuration
Before using the image processing tools, you need to set up the `config.yaml` file:
1. Specify the path to the image you want to process and the step size for cutting in the `config.yaml` file.

Example `config.yaml` file:
```yaml
numpy_basics:
  image_path: 'data\\image_cat.bmp'
  step: '1'
```


## Running the Project
To use the image processing tools, follow these steps:
1. Open a command line or terminal.
2. Navigate to the directory where the `src\Image_Processing_Tools.py` script is located.
3. Enter the command `python Image_Processing_Tools.py`.


## Results
The scripts will process the input image according to the specified configurations, producing resized, vertically and horizontally cut images, and a composite image that combines all three results.


## FAQ
**Q:** Can these tools be used for batch processing of multiple images?
**A:** Currently, the scripts are designed for single-image processing. Batch processing functionality could be a future enhancement.


## Contributions
Contributions are welcome! If you have suggestions for improvements or new features, please submit a pull request or create an issue.


## License
This project is distributed under the MIT license. See the LICENSE.txt file for details.
