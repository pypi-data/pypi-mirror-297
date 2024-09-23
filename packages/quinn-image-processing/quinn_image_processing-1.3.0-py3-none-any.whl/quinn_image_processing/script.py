import os
from PIL import Image

# Resize and crop the image in multiple ways (top-left, bottom-right, center)
def resize_and_crop_image(image_path, max_size, output_directory, enable_top_left_crop, enable_bottom_right_crop, enable_center_crop):
    """
    Resize and crop the image into selected versions (top-left, bottom-right, center).
    Replace any transparent pixels with white.
    """
    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            ratio = max(max_size / original_width, max_size / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Top-left crop
            if enable_top_left_crop:
                print(f"Processing top-left crop for {os.path.basename(image_path)}...")
                top_left_crop = resized_img.crop((0, 0, max_size, max_size))
                top_left_crop = replace_transparent_pixels(top_left_crop)
                save_cropped_image(top_left_crop, image_path, output_directory, "top_left", max_size)

            # Bottom-right crop
            if enable_bottom_right_crop:
                print(f"Processing bottom-right crop for {os.path.basename(image_path)}...")
                bottom_right_crop = resized_img.crop((new_width - max_size, new_height - max_size, new_width, new_height))
                bottom_right_crop = replace_transparent_pixels(bottom_right_crop)
                save_cropped_image(bottom_right_crop, image_path, output_directory, "bottom_right", max_size)

            # Center crop
            if enable_center_crop:
                print(f"Processing center crop for {os.path.basename(image_path)}...")
                left = (new_width - max_size) // 2
                top = (new_height - max_size) // 2
                center_crop = resized_img.crop((left, top, left + max_size, top + max_size))
                center_crop = replace_transparent_pixels(center_crop)
                save_cropped_image(center_crop, image_path, output_directory, "center", max_size)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def replace_transparent_pixels(image):
    """
    Replace transparent pixels in an image with white. 
    Convert from RGBA to RGB if the image has transparency.
    """
    if image.mode in ("RGBA", "LA"):  # Check for transparency
        return convert_transparent_to_white(image)
    return image

def save_cropped_image(cropped_img, image_path, output_directory, crop_type, max_size):
    """
    Save the cropped image to the specified output directory.
    """
    try:
        filename, ext = os.path.splitext(os.path.basename(image_path))
        output_filename = f"{filename}_{crop_type}_{max_size}x{max_size}{ext}"
        # Preserve the subdirectory structure in the output directory
        subdir_path = os.path.relpath(os.path.dirname(image_path), os.path.dirname(output_directory))
        output_dir_with_subfolders = os.path.join(output_directory, subdir_path)
        os.makedirs(output_dir_with_subfolders, exist_ok=True)

        output_path = os.path.join(output_dir_with_subfolders, output_filename)
        cropped_img.save(output_path)
        full_output_path = os.path.abspath(output_path)
        print(f"Saved {crop_type} image to {full_output_path}")
    except Exception as e:
        print(f"Error saving cropped image: {e}")

def resize_images_in_directory_for_crops(directory, max_size, output_directory, enable_top_left_crop, enable_bottom_right_crop, enable_center_crop):
    """
    Resizes and crops images in the given directory and its subdirectories 
    into selected crop options (top-left, bottom-right, center).
    Any transparent pixels in cropped images will be replaced with white.
    """
    supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

    # Walk through all subdirectories and process images
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip files with "_Generated_" in the path
            if "_Generated_" in file_path:
                print(f"Skipping {file_path} (contains '_Generated_')")
                continue

            if filename.lower().endswith(supported_extensions):
                try:
                    resize_and_crop_image(file_path, max_size, output_directory, enable_top_left_crop, enable_bottom_right_crop, enable_center_crop)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Resize and pad the image with white background
def resize_and_pad_image(image_path, max_size, output_directory):
    """
    Resize an image so that the larger dimension matches max_size (e.g., 2000 pixels),
    while maintaining the original aspect ratio. Then, pad the image with white to
    make it max_size x max_size pixels. For PNGs with transparent pixels, fill those areas with white.
    """
    try:
        with Image.open(image_path) as img:
            # Convert transparent areas in PNG to white
            if img.mode == "RGBA":
                img = convert_transparent_to_white(img)

            # Get original dimensions
            original_width, original_height = img.size

            # Calculate the ratio for resizing
            if original_width > original_height:
                ratio = max_size / original_width
            else:
                ratio = max_size / original_height

            # Calculate new dimensions
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a new image with a white background
            new_image = Image.new("RGB", (max_size, max_size), (255, 255, 255))

            # Calculate position to center the resized image
            paste_position = ((max_size - new_width) // 2, (max_size - new_height) // 2)

            # Paste the resized image onto the white square background
            new_image.paste(resized_img, paste_position)

            # Create output path and preserve subdirectory structure
            filename, ext = os.path.splitext(os.path.basename(image_path))
            output_filename = f"{filename}_padded_{max_size}x{max_size}{ext}"
            subdir_path = os.path.relpath(os.path.dirname(image_path), os.path.dirname(output_directory))
            output_dir_with_subfolders = os.path.join(output_directory, subdir_path)
            os.makedirs(output_dir_with_subfolders, exist_ok=True)

            output_path = os.path.join(output_dir_with_subfolders, output_filename)
            new_image.save(output_path)
            full_output_path = os.path.abspath(output_path)
            print(f"Saved padded image to {full_output_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def convert_transparent_to_white(image):
    """
    Convert an RGBA image (with transparency) to RGB, filling transparent pixels with white.
    """
    # Create a white background image
    background = Image.new("RGB", image.size, (255, 255, 255))
    
    # Paste the image on top of the white background, using the alpha channel as a mask
    background.paste(image, mask=image.split()[3])  # Use the alpha channel as the mask
    
    return background

def resize_images_in_directory_for_padding(directory, max_size, output_directory):
    """
    Resizes all image files in the given directory and its subdirectories
    so that the largest dimension matches max_size and pads them to make them max_size x max_size pixels.
    PNG images with transparent pixels will have those pixels filled with white.
    """
    supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

    # Walk through all subdirectories and process images
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip files with "_Generated_" in the path
            if "_Generated_" in file_path:
                print(f"Skipping {file_path} (contains '_Generated_')")
                continue

            if filename.lower().endswith(supported_extensions):
                try:
                    resize_and_pad_image(file_path, max_size, output_directory)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

def get_user_input():
    """
    Get user input for max image size for both crops and padding.
    """
    max_size = int(input("Enter the maximum size for the larger dimension (default is 2000): ") or 2000)
    return max_size

def main():
    # Directory containing the images
    image_directory = input("Enter the directory containing the images: ").strip()

    # Get user input for max image size
    max_image_size = get_user_input()

    # Ask the user for the folder name for processed images
    processed_folder_name = input("Enter a name for the processed images folder (default is 'ProcessedImages'): ").strip() or "ProcessedImages"
    processed_folder_name += '_Generated_'
    
    # Create output directory for all processed images
    output_directory = os.path.join(image_directory, processed_folder_name)
    os.makedirs(output_directory, exist_ok=True)

    # Ask the user which crop options to enable
    enable_top_left_crop = input("Do you want to enable Top-Left Crop? (y/n): ").strip().lower() == 'y'
    enable_bottom_right_crop = input("Do you want to enable Bottom-Right Crop? (y/n): ").strip().lower() == 'y'
    enable_center_crop = input("Do you want to enable Center Crop? (y/n): ").strip().lower() == 'y'
    
    # Ask if Resize and Pad is enabled
    enable_resize_and_pad = input("Do you want to enable Resize and Pad? (y/n): ").strip().lower() == 'y'

    # Run Resize and Crop (top-left, bottom-right, center) if any crop option is enabled
    if enable_top_left_crop or enable_bottom_right_crop or enable_center_crop:
        print("Running Resize and Crop...")
        resize_images_in_directory_for_crops(
            image_directory, 
            max_image_size, 
            output_directory, 
            enable_top_left_crop, 
            enable_bottom_right_crop, 
            enable_center_crop
        )
    else:
        print("Skipping Resize and Crop...")

    # Run Resize and Pad (with white background) if enabled
    if enable_resize_and_pad:
        print("Running Resize and Pad...")
        resize_images_in_directory_for_padding(image_directory, max_image_size, output_directory)
    else:
        print("Skipping Resize and Pad...")

if __name__ == "__main__":
    main()
