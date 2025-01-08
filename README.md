# H-Pasture Dataset
The H-Pasture Dataset is a repository of pasture images used to train and validate convolutional neural network (CNN) models. These models can estimate the average vegetation height directly from photographs quickly and conveniently. 

This [dataset](https://drive.google.com/drive/folders/1vRrVYCH6wE5pwK7oNJGpyfpCUxFNgKYS?usp=sharing) was developed as part of the master's thesis "Application of Convolutional Neural Networks in Estimating the Height of Native and Cultivated Pastures". The research introduced an approach that applies computer vision techniques to estimate the average height of three types of pastures: native vegetation from southern Brazilian fields, ryegrass (*Lolium multiflorum L.*), and sudangrass (*Sorghum sudanense L.*).

---

## Repository Purpose
This repository was created to share the H-Pasture Dataset, fostering research on the application of computer vision in agriculture. It also serves as a resource for experimenting with and developing machine learning models.

---

## Method for Photo Collection
To construct the dataset, a standardized photo collection process was implemented to ensure consistency and reliability. At each sampling point, a 0.25 m² frame was positioned over the vegetation to serve as a reference point (Figure 1-A). Within this frame, five height measurements were taken, and their average was recorded using the **H-Pasture Collector** app.

After the measurements were logged, the frame was removed, and photos were captured with the central area of the frame always aligned at the center of the images. The photo capture process (illustrated in Figure 1-B) involved taking pictures from varying distances between the camera and the vegetation (0.5 m, 1 m, 2 m, and 3 m) and from different angles (0°, 90°, 180°, and 270°) relative to the reference point. This method generated approximately 16 photos for each sampling point.

For sudangrass, however, photos were taken only from distances of 1 m, 2 m, and 3 m, resulting in 12 photos per sampling point. The entire procedure was repeated across all sampling points to ensure a comprehensive representation of vegetation under various conditions. Examples of photos captured for each vegetation type are presented in Figure 1-C.

**Figure 1 – Method for collecting photos**
![Figure 1 – Method for collecting photos](https://github.com/user-attachments/assets/393f69a1-11dd-4a15-b4e5-8948b9f0f497)

---

## Dataset Structure

The dataset for this project, due to its size, is stored on **Google Drive** and can be accessed through the following link: [Download the dataset](https://drive.google.com/drive/folders/1vRrVYCH6wE5pwK7oNJGpyfpCUxFNgKYS?usp=sharing)

The dataset is organized as follows:

- **Images**: Photographs are organized by vegetation type (`native`, `ryegrass`, `sudangrass`) in separate folders. Each folder contains images and a `mapping.json` file that maps each photo to its corresponding average vegetation height.

- **File Naming Convention**:  
  Each collection can contain up to 16 photos, stored in files named using the format `COLLECTIONID_SEQUENTIALNUMBER`. In this naming convention:
  - **COLLECTIONID**: Represents the unique identifier for the collection (key `Id`).
  - **SEQUENTIALNUMBER**: A sequential number from 0 to 15, used to distinguish the images associated with the same collection.

- **Mapping File**:  
  The `mapping.json` file inside each vegetation folder maps the photos to the measured average height of the vegetation. This file is structured as a list of mappings, where each entry contains the following keys:
  - **Id**: The unique identifier of the collection.
  - **ForageType**: The type of vegetation collected, such as ryegrass, native, or sudangrass.
  - **Mean**: The average vegetation height for the collection, measured in centimeters (cm).
  - **StandardDeviation** and **Distance**: Included in the file format but not utilized in the dataset.

---

## Scripts

The repository includes the following scripts:

- **`download.py`**: Downloads the dataset directly from Google Drive and organizes it in the `dataset/` folder. This script automates the download process for easier access to the data.

- **`preprocessing.py`**: Reads the `dataset/` folder based on the selected vegetation type and generates a set of images for training and validating convolutional neural networks. This script supports data augmentation and organizes the output into `training` and `test` folders.

Both scripts are located in the `scripts/` folder and include logging to track their progress. Be sure to check the usage instructions in the comments within each script.

---

## How to Contribute
Contributions are welcome! Feel free to open issues or submit pull requests with improvements, fixes, or suggestions.
