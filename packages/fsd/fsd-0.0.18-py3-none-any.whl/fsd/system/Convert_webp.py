import os
from PIL import Image

def convert_and_replace_webp(input_path, output_format):
    """
    Convert a WebP image to the specified format and delete the original WebP file.

    :param input_path: Path to the input WebP image.
    :param output_format: Desired output format ('jpg' or 'png').
    """
    try:
        # Open the WebP image
        img = Image.open(input_path)
    except IOError:
        print(f"Cannot open image file {input_path}")
        return

    # Determine the output path by replacing the file extension
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.{output_format.lower()}"

    try:
        if output_format.lower() in ('jpg', 'jpeg'):
            # Convert image to RGB mode for JPG format (JPG doesn't support transparency)
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, 'JPEG')
        elif output_format.lower() == 'png':
            img.save(output_path, 'PNG')
        else:
            print(f"Unsupported output format: {output_format}")
            return

        print(f"Converted {input_path} to {output_path}")

        # Delete the original WebP file
        os.remove(input_path)
        print(f"Deleted original WebP file {input_path}")

    except Exception as e:
        print(f"Failed to convert {input_path}: {e}")
