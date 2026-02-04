import os
import imghdr # To verify if a file is an image

def rename_images_in_folder(folder_path, prefix="ID_", start_number=1):
    """
    Renames all image files in a specified folder sequentially.

    Args:
        folder_path (str): The path to the folder containing the images.
        prefix (str): The prefix to use for the new image names (e.g., "my_photo_").
        start_number (int): The starting number for the sequential renaming.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    print(f"Starting to rename images in: {folder_path}")
    renamed_count = 0
    skipped_count = 0

    # Get a sorted list of all files in the directory
    # Sorting ensures consistent renaming order, though exact order might vary
    # depending on OS file system specifics if not sorted by creation date/modification date
    files = sorted(os.listdir(folder_path))

    for filename in files:
        old_file_path = os.path.join(folder_path, filename)

        # Check if it's a file and an actual image
        if os.path.isfile(old_file_path) and imghdr.what(old_file_path):
            # Get the file extension (e.g., .jpg, .png)
            _, file_extension = os.path.splitext(filename)

            # Construct the new filename
            new_filename = f"{prefix}{start_number:04d}{file_extension}" # :04d pads with leading zeros (e.g., 0001, 0002)
            new_file_path = os.path.join(folder_path, new_filename)

            try:
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
                renamed_count += 1
                start_number += 1 # Increment for the next image
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")
                skipped_count += 1
        else:
            # Skip non-image files or directories
            # print(f"Skipping non-image file or directory: '{filename}'") # Uncomment for verbose skipping
            skipped_count += 1

    print(f"\nRenaming complete!")
    print(f"Total images renamed: {renamed_count}")
    print(f"Total files skipped (non-images or errors): {skipped_count}")

# --- How to use the function ---
if __name__ == "__main__":
    # IMPORTANT:
    # 1. Replace 'path/to/your/images_folder' with the actual path to your folder.
    # 2. Make sure you have a backup of your images before running this,
    #    as file renaming is a destructive operation!

    # Example Usage:
    # Create a dummy folder and some dummy image files for testing
    test_folder = "C:/Users/PMLS/Desktop/Interior esign AI App/Dataset/images"


    # Example 2: Using the default prefix and start number
    rename_images_in_folder(test_folder)


