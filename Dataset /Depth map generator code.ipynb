import os
import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm
import torch as tch
from transformers import DPTForDepthEstimation, DPTImageProcessor


# Setupo MiDaS Model for Depth Estimation

model_name = "Intel/dpt-hybrid-midas"
image_processor = DPTImageProcessor.from_pretrained(model_name)
model = DPTForDepthEstimation.from_pretrained(model_name)

# Move Model to GPU if available

device = tch.device("cuda" if tch.cuda.is_available() else "cpu")
model.to(device)
model.eval()   # set model to evaluation mode

def create_depth_map(image_folder, annotation_folder):
    # process Image
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', 'jpeg'))]
    print(f"Found {len(image_files)} images in '{image_folder}'. Starting processing...")

    if not image_files:
        print("No images found in the input folder. Please check the path and image types.")
        return

    for image_file in tqdm(image_files, desc = "Processing images"):
        input_image_path = os.path.join(image_folder, image_file)
        base_name = os.path.splitext(image_file)[0] # Get filename without extension

        try:
            #  Load the image using PIL for MiDaS
            pil_image = Image.open(input_image_path).convert("RGB") # MiDaS expects RGB
            # cv_image = cv2.imread(input_image_path) # OpenCV reads BGR by default

            # if cv_image is None:
            #    print(f"Warning: Could not read image {image_file}. Skipping.")
            #    continue

            # Generate Depth Map

            with tch.no_grad(): # No need to calculate gradients for inference
                # Prepare image for MiDaS model
                inputs = image_processor(images = pil_image, return_tensors="pt")
                # Move inputs to the same evice as the model
                for k, v in inputs.items():
                    inputs[k] = v.to(device)

                #predict depth
                outputs = model(**inputs)
                prediction = outputs.predicted_depth # Assign the actual prediction to 'prediction'
                prediction = prediction.squeeze().cpu().numpy()

                # Normalize depth map to 0-255 for visualization and saving. This scaling makes the depth map visually discernible
                normalized_depth = (prediction - np.min(prediction)) / (np.max(prediction) - np.min(prediction))
                normalized_depth_uint8 = (normalized_depth * 255).astype(np.uint8)

                # You can apply a colormap for better visualization if needed,
                # but saving as grayscale is often preferred for "data"
                # depth_colored = cv2.applyColorMap(normalized_depth_uint8, cv2.COLORMAP_JET)

            depth_output_path = os.path.join(annotation_folder, f"{base_name}_depth.png")
            cv2.imwrite(depth_output_path, normalized_depth_uint8) # Save as grayscale PNG
            # If you want to save the colored version:
            # cv2.imwrite(depth_output_path, depth_colored)

        except Exception as e:
            print(f"Error processing {image_file}: {e}")


    print("\nDataset generation complete!")
    print(f"Depth and Canny images saved to '{annotation_folder}'")
           


if __name__ == "__main__":
    # IMPORTANT: Replace 'path/to/your/input_images' with the actual path to your 1500 images
    input_images_directory = "images/" # Example: Make sure this folder exists and contains your images
    output_annotations_directory = "annotation/"

    create_depth_map(input_images_directory, output_annotations_directory)
