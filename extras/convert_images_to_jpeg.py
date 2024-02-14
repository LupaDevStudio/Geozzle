import os
from PIL import Image

main_folder_path = "resources/images/continents/"

images_list = os.listdir(main_folder_path)
for image_name in images_list:
    image = Image.open(main_folder_path + image_name)
    image.save(main_folder_path +
               image_name.replace(".png", ".jpg"), optimize=True)
    os.remove(main_folder_path + image_name)
