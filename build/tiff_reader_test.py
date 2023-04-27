import rasterio
import os
import imageio
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from build.network_lib.functions.network_functions import load_trained_model, predict_class
from build.network_lib.functions.math_functions import convert_truths_to_integer


def read_tiff_collection(dir_path):
    filenames = [f for f in os.listdir(dir_path) if f.endswith(".tif")]

    num_samples = len(filenames)
    data = np.zeros((num_samples, 64, 64, 125))
    bounds = np.zeros((num_samples, 2, 2))

    for i, filename in enumerate(filenames):
        image = imageio.imread(os.path.join(dir_path, filename))
        if image.shape[-1] == 126:
            image = image[..., :125]
        data[i, :, :, :] = image

        with rasterio.open(os.path.join(dir_path, filename)) as src:
            bounds[i, 0, 0] = src.bounds.left
            bounds[i, 0, 1] = src.bounds.bottom
            bounds[i, 1, 0] = src.bounds.right
            bounds[i, 1, 1] = src.bounds.top
    
    return data, bounds


def plot_square(ax, x1, y1, x2, y2, color):
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    square = Rectangle((x1, y1), width, height, facecolor=color)
    ax.add_patch(square)

    return ax

def save_as_png(img: np.ndarray, filename: str):
    """
    Save a 3-channel NumPy array as a PNG image.
    
    Parameters:
        img (numpy.ndarray): 3-channel NumPy array representing the image
        filename (str): Name of the file to save the image to, including the .png extension
    """
    # Ensure that the image has a valid data type and shape for imageio
    img = img.astype(np.uint8)
    if img.shape[2] != 3:
        raise ValueError("Image must be a 3-channel (RGB) image")
    
    # Save the image as a PNG file using imageio
    imageio.imwrite(filename, img)

def load_png_into_array(filename):
    # Read the image data into a NumPy array
    np_img = imageio.imread(filename)

    # Drop the alpha channel if present and reshape to 3 channels
    if np_img.ndim == 3 and np_img.shape[2] == 4:
        np_img = np_img[:, :, :3]

    return np_img

def convert_to_greyscale(img: np.ndarray) -> np.ndarray:
    """
    Convert a 3-channel NumPy image to grayscale while preserving the 3 color channels.
    
    Parameters:
        img (numpy.ndarray): 3-channel NumPy array representing the image
    
    Returns:
        numpy.ndarray: 3-channel NumPy array representing the grayscale image with the same shape as the input image.
    """
    # Check that the image has 3 color channels
    if img.shape[2] != 3:
        raise ValueError("Image must have 3 color channels")
    
    # Compute the grayscale value for each pixel using the luminosity method
    grey_vals = np.dot(img, [0.2989, 0.5870, 0.1140])
    
    # Create a new 3-channel image with the grayscale value repeated across all channels
    new_img = np.repeat(grey_vals[..., np.newaxis], 3, axis=-1)
    
    return new_img

def convert_to_rgb(img):
    # Normalize the image
    img = (img - np.min(img)) / (np.max(img) - np.min(img))
    
    # Create an empty array for the RGB image
    height, width, channels = img.shape
    rgb_img = np.zeros((height, width, 3))
    
    # Assign the R, G, and B channels
    rgb_img[:,:,0] = img[:,:,0] # Red channel
    rgb_img[:,:,1] = img[:,:,1] # Green channel
    rgb_img[:,:,2] = img[:,:,2] # Blue channel
    
    return rgb_img

def draw_transparent_square(img: np.ndarray, x1: int, y1: int, x2: int, y2: int, color: tuple, alpha: float) -> np.ndarray:
    """
    Draw a transparent square on a 3-channel NumPy array.
    
    Parameters:
        img (numpy.ndarray): 3-channel NumPy array representing the image
        x1 (int): x-coordinate of the top-left corner of the square
        y1 (int): y-coordinate of the top-left corner of the square
        x2 (int): x-coordinate of the bottom-right corner of the square
        y2 (int): y-coordinate of the bottom-right corner of the square
        color (tuple): RGB color of the square as a tuple of integers between 0 and 255
        alpha (float): Transparency level of the square, as a value between 0 (fully transparent) and 1 (fully opaque)
        
    Returns:
        numpy.ndarray: 3-channel NumPy array with the square drawn on it
    """
    # Convert the color to a NumPy array
    color = np.array(color, dtype=np.uint8)
    
    # Create a mask for the square
    mask = np.zeros_like(img)
    size = 12 * 64
    mask[size-y2:size-y1, x1:x2, :] = color
    
    # Combine the mask with the original image using alpha blending
    #blended = img + mask

    #blended = alpha * mask + (1 - alpha) * img

    blended = convert_to_greyscale(img) * (mask/256) * np.where(mask == 0, 0, 1) + img * np.where(mask == 0, 1, 0)

    return blended

def create_overlay_image(model_path, data_folder_path, background_image_path, output_file_path):
    '''
    Creates an image overlay of multiple tiffs

    Parameters:
        model_path (str): path towards the model to generate outputs
        data_folder_path (str): path towards the data folder in which the function will itterate over
        background_image_path (str): path towards the background image in which to overlay onto
        output_file_path (str): path to and name of the image to be generated

    Returns:
        None
    
    Example Usage:
        create_overlay_image("build\\network_lib\\saved_models\\trained_model_2023-04-26_01-32-42.h5", 
                             "C:\\Users\\binar\\Downloads\\set1_edited_12x12\\set1_edited", 
                             "image.png",
                             "test.png")
    '''
    data, bounds = read_tiff_collection(data_folder_path) # "C:\\Users\\binar\\Downloads\\set1_edited_12x12\\set1_edited"
    model = load_trained_model(model_path) # "build\\network_lib\\saved_models\\trained_model_2023-04-26_01-32-42.h5"
    predictions = predict_class(model, data)

    size = int(bounds.max())
    tiff_image_size = 64
    image = load_png_into_array(background_image_path)

    for i in range(data.shape[0]):
        if predictions[i] == 0:     color_rgb = (255*100,0,0)
        elif predictions[i] == 1:   color_rgb = (0,255*100,0)
        else:                   color_rgb = (200,200,200)

        image = draw_transparent_square(image, 
                                        int(bounds[i, 0, 0]*tiff_image_size), int(bounds[i, 0, 1]*tiff_image_size),
                                        int(bounds[i, 1, 0]*tiff_image_size), int(bounds[i, 1, 1]*tiff_image_size),
                                        color_rgb, 0.2)

    save_as_png(image, output_file_path)

create_overlay_image("build\\network_lib\\saved_models\\trained_model_2023-04-26_01-32-42.h5", 
                             "C:\\Users\\binar\\Downloads\\set1_edited_12x12\\set1_edited", 
                             "image.png",
                             "test.png")