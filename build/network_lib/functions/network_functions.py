import os
import numpy as np
import imageio
from keras.models import load_model

## Loading Data
def load_tiff_data(dir_path):
    filenames = [f for f in os.listdir(dir_path) if f.endswith(".tif")]
    num_samples = len(filenames)
    data = np.zeros((num_samples, 64, 64, 125))
    truth = np.zeros((num_samples, 3))
    
    for i, filename in enumerate(filenames):
        image = imageio.imread(os.path.join(dir_path, filename))
        if image.shape[-1] == 126:
            image = image[..., :125]
        data[i, :, :, :] = image
        
        if "Health" in filename:
            truth[i, 0] = 1
        elif "Rust" in filename:
            truth[i, 1] = 1
        else:
            truth[i, 2] = 1
            
    return data, truth

def load_single_tiff(file_path):
    image = imageio.imread(file_path)
    if image.shape[-1] == 126:
        image = image[..., :125]
    return image

def extract_and_return_remaining_data(data, truth, num_samples):
    indices = np.random.choice(data.shape[0], num_samples, replace=False)
    extracted_data = data[indices]
    extracted_truth = truth[indices]
    remaining_data = np.delete(data, indices, axis=0)
    remaining_truth = np.delete(truth, indices, axis=0)
    return extracted_data, extracted_truth, remaining_data, remaining_truth

def randomize_data(data, truth):
    num_samples = data.shape[0]
    permutation = np.random.permutation(num_samples)
    randomized_data = data[permutation]
    randomized_truth = truth[permutation]
    return randomized_data, randomized_truth

## Loading model
def load_trained_model(model_file_path):
    model = load_model(model_file_path)
    return model

## Augmentation Functions
def augment_data(data, truth):
    data, truth = augment_data_by_flipping_vertically(data, truth)
    data, truth = augment_data_by_rotating(data, truth)
    return data, truth

def augment_data_by_flipping_vertically(data, truth):
    flipped_data = np.flip(data, axis=2)
    augmented_data = np.concatenate((data, flipped_data), axis=0)
    augmented_truth = np.concatenate((truth, truth), axis=0)
    return augmented_data, augmented_truth

def augment_data_by_rotating(data, truth):
    rotated_data = np.rot90(data, k=1, axes=(1, 2))
    augmented_data = np.concatenate((data, rotated_data), axis=0)
    augmented_truth = np.concatenate((truth, truth), axis=0)
    return augmented_data, augmented_truth

""" def random_crop(data, truths, crop_size=(32, 32, 125), overlap=0.25):
    num_samples, h, w, c = data.shape
    crop_h, crop_w, crop_c = crop_size
    assert h >= crop_h and w >= crop_w and c == crop_c, "Crop size should not be larger than the original image size"
    max_overlap_h = int(crop_h * overlap)
    max_overlap_w = int(crop_w * overlap)
    crops = []
    truths_crops = []
    for i in range(num_samples):
        attempts = 0
        while attempts < 5:
            x = np.random.randint(0, h - crop_h + 1)
            y = np.random.randint(0, w - crop_w + 1)
            crop = data[i, x:x+crop_h, y:y+crop_w, :]
            overlap_flag = False
            for prev_crop in crops:
                h_overlap = min(x + crop_h, prev_crop[0] + crop_h) - max(x, prev_crop[0])
                w_overlap = min(y + crop_w, prev_crop[1] + crop_w) - max(y, prev_crop[1])
                if h_overlap > max_overlap_h and w_overlap > max_overlap_w:
                    overlap_flag = True
                    break
            if not overlap_flag:
                crops.append((x, y))
                truths_crops.append(truths[i])
                break
            attempts += 1
    crops = np.stack(crops, axis=0)
    truths_crops = np.stack(truths_crops, axis=0)
    return crops, truths_crops """

def predict_class(model, data):
  predictions = model.predict(data)
  return np.argmax(predictions, axis=1)