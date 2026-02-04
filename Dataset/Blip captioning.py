import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from tqdm import tqdm
import json

# --- 1. Setup BLIP Model for Image Captioning ---
print("Loading BLIP image captioning model...")
blip_model_name = "Salesforce/blip-image-captioning-base"
blip_processor = BlipProcessor.from_pretrained(blip_model_name)
blip_model = BlipForConditionalGeneration.from_pretrained(blip_model_name)


# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
blip_model.to(device)
blip_model.eval()   # Set BLIP model to evaluation mode


def generate_image_captions(input_folder, output_folder, annotation_image_folder, json_filename="metadata.json"):

    # --- 2. Process Images ---
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', 'jpeg'))]
    print(f"Found {len(image_files)} images in '{input_folder}'. Starting captioning...")

    if not image_files:
        print("No images found in the input folder. Please check the path and image types.")
        return

    # List to store caption data for JSON
    caption_data = []

    for image_file in tqdm(image_files, desc="Generating captions"):
        input_image_path = os.path.join(input_folder, image_file)
        base_name = os.path.splitext(image_file)[0] # Get filename without extension

        try:
            pil_image = Image.open(input_image_path).convert("RGB") # PIL Image for BLIP model

            # --- Generate Image Caption ---
            with torch.no_grad():
                # Prepare image for BLIP model
                blip_inputs = blip_processor(images=pil_image, return_tensors="pt")
                # Move inputs to the same device as the model
                for k, v in blip_inputs.items():
                    blip_inputs[k] = v.to(device)

                # Generate caption
                # `max_length` and `num_beams` can be tuned for caption quality/length
                generated_ids = blip_model.generate(**blip_inputs, max_length=50, num_beams=5)
                generated_caption = blip_processor.decode(generated_ids[0], skip_special_tokens=True)

            # --- Construct Annotation File Path ---
            # Assuming depth maps are named like 'original_image_name_depth.png'
            # Adjust this if your annotation files have a different naming convention or type
            annotation_file_name = f"{base_name}_depth.png"
            full_annotation_file_path = os.path.join(annotation_image_folder, annotation_file_name)

            # Check if the annotation file actually exists (optional, but good for robustness)
            if not os.path.exists(full_annotation_file_path):
                print(f"Warning: Annotation file '{full_annotation_file_path}' not found for '{image_file}'. Skipping its inclusion.")
                full_annotation_file_path = None # Set to None or some placeholder if not found


            # Store data for JSON
            # For ControlNet, 'file_name' usually refers to the ORIGINAL image.
            caption_data.append({
                "file_name": image_file, # Use the original image filename
                "annotation_file": full_annotation_file_path, # Now correctly defined
                "text": generated_caption
            })

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

    # --- 3. Save Captions to JSON File ---
    json_output_path = os.path.join(output_folder, json_filename)
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(caption_data, f, ensure_ascii=False, indent=4)

    print("\nCaption generation complete!")
    print(f"Captions saved to '{json_output_path}'")

# --- How to use the function ---
if __name__ == "__main__":
    # IMPORTANT: Replace these paths with your actual directories
    input_images_directory = "/content/drive/MyDrive/images/"
    output_captions_directory = "/content/drive/MyDrive/captioning/"
    annotation_images_directory = "/content/drive/MyDrive/annotation/" # Assuming your depth maps are here

    # Call the function to generate the captions
    generate_image_captions(
        input_images_directory,
        output_captions_directory,
        annotation_images_directory # Pass the annotation folder here
    )



# Replace a annotation file path with correct path in matadata jason file
caption_file = "/content/drive/MyDrive/Controlnet_Finetune_Project/captioning/metadata.json"

def replace_word_in_file(filepath, old_word, new_word):
    """
    Replaces all occurrences of a specific word in a file with a new word.

    Args:
        filepath (str): The path to the file.
        old_word (str): The word to be replaced.
        new_word (str): The word to replace with.
    """
    try:
        # Read the entire content of the file
        with open(filepath, 'r') as file:
            file_content = file.read()

        # Perform the replacement
        modified_content = file_content.replace(old_word, new_word)

        # Write the modified content back to the file
        with open(filepath, 'w') as file:
            file.write(modified_content)

        print(f"Successfully replaced '{old_word}' with '{new_word}' in '{filepath}'.")

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_to_modify = "my_document.txt"
word_to_find = "old_text"
word_to_replace = "new_text"

# Create a dummy file for demonstration
with open(file_to_modify, 'w') as f:
    f.write("This is some old_text in the document.\n")
    f.write("Another line with old_text.\n")

replace_word_in_file(file_to_modify, word_to_find, word_to_replace)

with open(caption_file, 'r', encoding='utf-8') as f:
            caption_data = json.load(f)

samples = []
for entry in caption_data:
   annotation_image_path = Path(entry["annotation_file"])

