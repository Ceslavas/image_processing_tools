import numpy as np
from PIL import Image
import yaml
from typing import Tuple, Dict


class ConfigLoader:
    """
    A class used to load and validate configuration data from a YAML file.
    """
    
    @staticmethod
    def load_config(config_path: str) -> Dict:
        """
        Loads configuration from the given YAML file path.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            Dict: Configuration data as a dictionary.

        Raises:
            FileNotFoundError: If the configuration file is not found at the specified path.
        """
        try:
            with open(config_path, "r", encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at path: {config_path}")

    @staticmethod
    def validate_config(config: Dict) -> Tuple[str, int]:
        """
        Validates the configuration data, ensuring required fields are present.

        Args:
            config (Dict): Configuration data to validate.

        Returns:
            Tuple[str, int]: Tuple containing image_path and step, if valid.

        Raises:
            ValueError: If the configuration data is invalid.
        """

        # Extracting image_path and step from the configuration data
        try:
            image_path = config['numpy_basics']['image_path']
            step_str = config['numpy_basics']['step']
        except KeyError:
            raise ValueError("Invalid configuration data. 'image_path' or 'step' is missing.")

        # Validating the step value:
        # The step value should be an integer and within the allowed range
        try:
            step = int(step_str)
        except ValueError:
            raise ValueError(f"The provided step value is not a valid integer: {step_str}")
        # The step value should be within the allowed range    
        try:
            image = Image.open(image_path)
            max_step_value = int(max(image.size) * 0.02)  # 2% of the image size
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found at path: {image_path}")

        if step < 1 or step > max_step_value:
            raise ValueError(f"The step value is not within the allowed range: 1 <= step <= {max_step_value}\nprovided step: {step}")

        return image_path, step



class ImageProcessor:
    """
    A class for processing images using operations like size adjustment, slicing, etc.
    """
    
    def __init__(self, step: int):
        """
        Initializes the ImageProcessor with a step for image processing.

        Args:
            step (int): The step size to use for slicing the image.
        """
        self.step = step

    def adjust_image_size(self, image: np.ndarray) -> np.ndarray:
        """
        Adjusts the image size to be a multiple of the step size.

        Args:
            image (np.ndarray): The input image as a NumPy array.

        Returns:
            np.ndarray: The adjusted image as a NumPy array.
        """
        h, w = image.shape[:2]
        w = w // self.step * self.step
        h = h // self.step * self.step
        return image[:h, :w]

    def cut_image(self, image: np.ndarray, axis: int) -> Image.Image:
        """
        Slices the image vertically or horizontally according to the given step.

        Args:
            image (np.ndarray): The input image as a NumPy array.
            axis (int): The axis along which to slice the image (0 for horizontal, 1 for vertical).

        Returns:
            Image.Image: The sliced image as a PIL Image object.
        """
        image = self.adjust_image_size(image)
        mask = np.arange(image.shape[axis]) // self.step % 2 == 0
        image_np_1 = image[mask] if axis == 0 else image[:, mask]
        image_np_2 = image[~mask] if axis == 0 else image[:, ~mask]
        result_image = np.concatenate([image_np_1, image_np_2], axis=axis)
        return Image.fromarray(result_image)

    def process_image(self, image_path: str) -> Image.Image:
        """
        Processes the image by performing vertical and horizontal slicing.

        Args:
            image_path (str): Path to the image file.

        Returns:
            Image.Image: The processed image containing original, vertical, and horizontal slices.

        Raises:
            FileNotFoundError: If the image file is not found at the specified path.
        """
        try:
            image = Image.open(image_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Image file not found at path: {image_path}") from e

        image_np = self.adjust_image_size(np.array(image))
        image = Image.fromarray(image_np)
        vertical_image = self.cut_image(image_np, axis=1)
        horizontal_image = self.cut_image(np.array(vertical_image), axis=0)
        all_images = np.concatenate([np.array(image), np.array(vertical_image), np.array(horizontal_image)], axis=0)

        return Image.fromarray(all_images)


def main():
    """
    Main function to load configuration, validate it, and process the image.
    """
    config_path = "config.yaml"
    try:
        config = ConfigLoader.load_config(config_path)
        image_path, step = ConfigLoader.validate_config(config)
        processor = ImageProcessor(step)
        all_images = processor.process_image(image_path)
        all_images.show()
    except (FileNotFoundError, ValueError) as e:
        print(e)


if __name__ == "__main__":
    main()
