import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize


def read_multiple_dicom_files(directory_path):
    try:
        # List all DICOM files in the directory
        dicom_files = [f for f in os.listdir(directory_path) if f.endswith('.dcm')]
        
        # Store pixel data from all DICOM files
        pixel_data_list = []
        
        for dicom_file in dicom_files:
            file_path = os.path.join(directory_path, dicom_file)
            dicom_data = pydicom.dcmread(file_path)
            
            # Print metadata
            print(f"Reading {dicom_file}:")
            print("Patient Name:", dicom_data.PatientName)
            print("Patient ID:", dicom_data.PatientID)
            print("Modality:", dicom_data.Modality)
            print("Study Date:", dicom_data.StudyDate)
            
            # Store pixel data if available
            if hasattr(dicom_data, "pixel_array"):
                pixel_data_list.append(dicom_data.pixel_array)
            else:
                print(f"No pixel data found in {dicom_file}.")
        
        # Combine all images into a single plot
        if pixel_data_list:
            _, axes = plt.subplots(1, len(pixel_data_list), figsize=(20, 10))  # Adjusted figure size
            if len(pixel_data_list) == 1:
                axes = [axes]  # Ensure axes is iterable if there's only one image
            
            for ax, pixel_data, dicom_file in zip(axes, pixel_data_list, dicom_files):
                ax.imshow(pixel_data, cmap="gray")
                ax.set_title(f"Image: {dicom_file}")
                ax.axis('off')
            
            # Adjust layout and spacing
            plt.subplots_adjust(wspace=0.5)  # Add spacing between subplots
            plt.show()
        else:
            print("No images to display.")
        return pixel_data_list
    
    except Exception as e:
        print(f"Error reading DICOM files: {e}")
        return []


directory_path = r"C:\Users\syedr\OneDrive\Desktop\DICOM\umap"  # Define your directory path here

pixel_data_list = read_multiple_dicom_files(directory_path)

        # Resize all images to the same shape
def combine_dicom_images(pixel_data_list):
    try:
        # Resize all images to the same shape
        target_shape = pixel_data_list[0].shape
        resized_images = [resize(image, target_shape, mode='constant') for image in pixel_data_list]
        
        # Combine all pixel data into a single image
        combined_image = np.sum(resized_images, axis=0)
        
        # Display the combined image
        plt.figure(figsize=(10, 10))
        plt.imshow(combined_image, cmap="gray")
        plt.title("Combined PET Scan Image")
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Error combining DICOM images: {e}")

# Call the function to combine and display the images
combine_dicom_images(pixel_data_list)