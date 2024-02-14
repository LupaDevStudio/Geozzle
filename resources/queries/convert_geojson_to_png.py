import json
from PIL import Image, ImageDraw

file_path = "countries.geojson"
img_side = 500

output_folder = "../images/countries_shape/"

with open(file_path, "r", encoding="utf-8") as file:
    geo_dict = json.load(file)

geo_dict = geo_dict["features"]

for country in geo_dict:
    current_ISO_code = country["properties"]["ISO_A3"]
    current_shape = country["geometry"]["coordinates"]
    current_shape_type = country["geometry"]["type"]
    current_image = Image.new(
        "RGBA", (img_side, img_side), (255, 255, 255, 255))
    current_image_draw = ImageDraw.Draw(current_image)
    if current_shape_type == "Polygon":
        x_list = [e[0] for e in current_shape[0]]
        y_list = [e[1] for e in current_shape[0]]
        x_min = min(x_list)
        x_max = max(x_list)
        y_min = min(y_list)
        y_max = max(y_list)
        if (x_max - x_min) > (y_max - y_min):
            norm_max = (x_max - x_min) * 1.1
            x_offset = (1 - (x_max - x_min) / norm_max) * img_side / 2
            y_offset = (1 - (y_max - y_min) / norm_max) * img_side / 2
        else:
            norm_max = (y_max - y_min) * 1.1
            x_offset = (1 - (x_max - x_min) / norm_max) * img_side / 2
            y_offset = (1 - (y_max - y_min) / norm_max) * img_side / 2
        x_list_norm = [(x - x_min) / norm_max
                       * img_side + x_offset for x in x_list]
        y_list_norm = [(y - y_min) / norm_max
                       * img_side + y_offset for y in y_list]
        coords_list = [(x_list_norm[i], img_side - y_list_norm[i])
                       for i in range(len(x_list))]
        current_image_draw.polygon(coords_list, fill=(
            0, 0, 0), outline=(0, 0, 0), width=10)
    else:
        # Compute extrema of the coordinates
        x_min = current_shape[0][0][0][0]
        x_max = current_shape[0][0][0][0]
        y_min = current_shape[0][0][0][1]
        y_max = current_shape[0][0][0][1]
        print("nb sub shapes", len(current_shape))
        for sub_shape in current_shape:
            temp_x_list = [e[0] for e in sub_shape[0]]
            temp_y_list = [e[1] for e in sub_shape[0]]
            temp_x_min = min(temp_x_list)
            temp_x_max = max(temp_x_list)
            temp_y_min = min(temp_y_list)
            temp_y_max = max(temp_y_list)
            if temp_x_min < x_min:
                x_min = temp_x_min
            if temp_x_max > x_max:
                x_max = temp_x_max
            if temp_y_min < y_min:
                y_min = temp_y_min
            if temp_y_max > y_max:
                y_max = temp_y_max
        # Compute coefficients to renormalize the coordinates
        if (x_max - x_min) > (y_max - y_min):
            norm_max = (x_max - x_min) * 1.1
            x_offset = (1 - (x_max - x_min) / norm_max) * img_side / 2
            y_offset = (1 - (y_max - y_min) / norm_max) * img_side / 2
        else:
            norm_max = (y_max - y_min) * 1.1
            x_offset = (1 - (x_max - x_min) / norm_max) * img_side / 2
            y_offset = (1 - (y_max - y_min) / norm_max) * img_side / 2

        for sub_shape in current_shape:
            x_list = [e[0] for e in sub_shape[0]]
            y_list = [e[1] for e in sub_shape[0]]

            x_list_norm = [(x - x_min) / norm_max
                           * img_side + x_offset for x in x_list]
            y_list_norm = [(y - y_min) / norm_max
                           * img_side + y_offset for y in y_list]
            coords_list = [(x_list_norm[i], img_side - y_list_norm[i])
                           for i in range(len(x_list))]
            current_image_draw.polygon(coords_list, fill=(
                0, 0, 0), outline=(0, 0, 0), width=10)
    # Save the image
    current_image.save(output_folder + current_ISO_code + ".png")
