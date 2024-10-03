import os
from PIL import Image

input_folder_path = "resources/images/backgrounds/"
output_folder_path = "resources/images/stickers/"

new_height = 256

for continent in os.listdir(input_folder_path):
    # Skip if the object is a file instead of a folder
    if continent.endswith(".jpg"):
        continue

    # Create the path to use
    local_input_folder = input_folder_path + continent + "/"
    local_output_folder = output_folder_path + continent + "/"

    # Create new folder if necessary
    if not os.path.exists(local_output_folder):
        os.mkdir(local_output_folder)

    # Iterate over the images inside the folder
    images_list = os.listdir(local_input_folder)
    for image_name in images_list:
        image = Image.open(local_input_folder + image_name)
        new_width = int(image.width * new_height / image.height)
        new_size = (new_width, 256)
        image = image.resize(new_size)
        image.save(local_output_folder +
                   image_name.replace(".png", ".jpg"), optimize=True)
