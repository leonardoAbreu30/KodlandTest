from PIL import Image
import os

# Set the directory containing your right-facing images
input_dir = "images"
output_dir = "images"  # Output in same folder

# List of hero image names to flip
images_to_flip = [
    "enemy_walk_1.png",
    "enemy_walk_2.png"
]

for img_name in images_to_flip:
    img_path = os.path.join(input_dir, img_name)
    img = Image.open(img_path)
    flipped = img.transpose(Image.FLIP_LEFT_RIGHT)

    name, ext = os.path.splitext(img_name)
    flipped_name = f"{name}_left{ext}"
    flipped.save(os.path.join(output_dir, flipped_name))

    print(f"Saved flipped image as {flipped_name}")
