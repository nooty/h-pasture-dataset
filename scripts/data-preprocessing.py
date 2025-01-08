import numpy as np
import os
from random import random, shuffle
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import json
import shutil
import sys

# Parameters
image_size = 720  # width and height
resize_size = 720
image_pixels = image_size * image_size

def log_message(message):
    """Helper function to log messages."""
    print(f"[INFO] {message}")

def create_dataset(folder):
    """Creates a dataset of images and corresponding heights."""
    log_message(f"Creating dataset from folder: {folder}")
    
    images = []
    heights = []

    mappings = load_mappings(folder)
    ids = []

    files = sorted(os.listdir(folder))
    log_message(f"Found {len(files)} files in {folder}")

    for file in files:
        image_path = os.path.join(folder, file)
        file_name, file_extension = os.path.splitext(file)

        if file_extension != '.jpg':
            continue

        image_id = get_file_id(file_name)
        ids.append(image_id)

        mapping = find_mapping(int(image_id), mappings)
        heights.append(float(mapping['Mean']))

        image = tf.keras.utils.load_img(image_path)
        input_arr = tf.keras.utils.img_to_array(image)
        images.append(np.array(input_arr))

    scaler = MinMaxScaler()
    heights = np.array(heights).reshape(-1, 1)
    heights = scaler.fit_transform(heights)

    log_message(f"Dataset created with {len(images)} images")
    return ids, images, heights

def load_mappings(folder):
    """Loads the mapping JSON file."""
    mapping_file = os.path.join(folder, 'mapping.json')
    log_message(f"Loading mappings from {mapping_file}")
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def find_mapping(image_id, mappings):
    """Finds the mapping for a given image ID."""
    return next(mapping for mapping in mappings if mapping['Id'] == image_id)

def get_file_id(file_name):
    """Extracts the file ID from the filename."""
    return file_name.split('_')[0]

def crop_to_square(image):
    """Crops the image to a square shape."""
    height, width, _ = image.shape
    size = min(height, width)
    start_x = (width - size) // 2
    return tf.image.crop_to_bounding_box(image, 0, start_x, size, size)

def save_image_without_augmentation(path, image_id, image, counter):
    """Saves an image without augmentation."""
    os.makedirs(path, exist_ok=True)
    img = tf.keras.utils.array_to_img(crop_to_square(image))
    save_path = f"{path}{image_id}_{counter}.jpg"
    keras.preprocessing.image.save_img(save_path, img)
    log_message(f"Saved image without augmentation: {save_path}")

def save_image_with_augmentation(path, image_id, image, counter):
    """Saves an image with augmentation."""
    os.makedirs(path, exist_ok=True)
    img = tf.keras.utils.array_to_img(crop_to_square(image))

    save_base = f"{path}{image_id}_{counter}"
    ref0b0 = tf.image.resize(img, [resize_size, resize_size])
    keras.preprocessing.image.save_img(f"{save_base}_r0_b0.jpg", ref0b0)

    ref0b0flip = tf.image.flip_left_right(img)
    keras.preprocessing.image.save_img(f"{save_base}_r0_b0_flip.jpg", ref0b0flip)

    log_message(f"Saved augmented images: {save_base}")

def main():
    # Parse vegetation type from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python data-preprocessing.py <vegetation_type>")
        print("Available options: native, ryegrass, sudangrass")
        sys.exit(1)

    species = sys.argv[1].lower()
    valid_species = ['native', 'ryegrass', 'sudangrass']
    
    if species not in valid_species:
        print(f"Invalid vegetation type: {species}")
        print(f"Available options: {', '.join(valid_species)}")
        sys.exit(1)

    output_species = species

    # Set the current working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    log_message(f"Current directory set to: {os.getcwd()}")

    # Create dataset
    ids, images, heights = create_dataset(os.path.join('dataset', species))

    # Split data into training and testing sets
    log_message("Splitting data into training and testing sets")
    counter = 0
    tests_count = 0

    for i in range(len(ids)):
        counter += 1
        rnd = random()

        if rnd <= 0.8:
            save_image_with_augmentation(f"output/{output_species}/training/", ids[i], images[i], counter)
            continue

        save_image_without_augmentation(f"output/{output_species}/test/", ids[i], images[i], counter)
        tests_count += 1

    # Copy a subset of training images to test_with_training
    log_message(f"Copying a subset of {tests_count} training images to test_with_training")
    os.makedirs(f"output/{output_species}/test_with_training", exist_ok=True)
    training_files = os.listdir(f"output/{output_species}/training")
    shuffle(training_files)
    selected_files = training_files[:tests_count]

    for file in selected_files:
        shutil.copyfile(f"output/{output_species}/training/{file}", f"output/{output_species}/test_with_training/{file}")

    # Copy mapping.json to the output folder
    log_message("Copying mapping.json to the output folder")
    shutil.copyfile(f"dataset/{species}/mapping.json", f"output/{output_species}/mapping.json")

    log_message("Data processing complete")

if __name__ == "__main__":
    main()
