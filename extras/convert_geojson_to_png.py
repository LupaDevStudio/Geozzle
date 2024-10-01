import json
from PIL import Image, ImageDraw
from math import log, tan, pi


def mercator_projection_x(long):
    return long * pi / 180


def mercator_projection_y(lat):
    if lat > 89:
        lat = 89
    elif lat < -89:
        lat = -89
    try:
        y = log(tan(lat * pi / 180 / 2 + pi / 4))
    except:
        raise ValueError(lat)
    return y


def mercator_projection(long, lat):
    """
    Compute mercator projection.

    Parameters
    ----------
    long : float
        Longitude in degree.
    lat : float
        Latitude in degree.

    Returns
    -------
    (float, float)
        Tuple of x and y coordinates.
    """

    x = mercator_projection_x(long)
    y = mercator_projection_y(lat)

    return x, y


file_path = "draft_countries.geojson"
img_side = 500

output_folder = "resources/images/countries_shape/"

with open(file_path, "r", encoding="utf-8") as file:
    geo_dict = json.load(file)

geo_dict = geo_dict["features"]

for country in geo_dict:
    current_ISO_code = country["properties"]["ISO_A3"]
    current_shape = country["geometry"]["coordinates"]
    current_shape_type = country["geometry"]["type"]
    current_image = Image.new(
        "RGBA", (img_side, img_side), (255, 255, 255, 0))
    current_image_draw = ImageDraw.Draw(current_image)
    if current_shape_type == "Polygon":
        long_list = [e[0] for e in current_shape[0]]
        lat_list = [e[1] for e in current_shape[0]]
        x_list = [mercator_projection_x(long) for long in long_list]
        y_list = [mercator_projection_y(lat) for lat in lat_list]
        x_min = min(x_list)
        x_max = max(x_list)
        y_min = min(y_list)
        y_max = max(y_list)
        if (x_max - x_min) > (y_max - y_min):
            norm_max = (x_max - x_min) * 1.1
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
            255, 255, 255), outline=(255, 255, 255), width=10)
    else:
        # Compute extrema of the coordinates
        x_min = mercator_projection_x(current_shape[0][0][0][0])
        x_max = mercator_projection_x(current_shape[0][0][0][0])
        y_min = mercator_projection_y(current_shape[0][0][0][1])
        y_max = mercator_projection_y(current_shape[0][0][0][1])
        print("nb sub shapes", len(current_shape))
        for sub_shape in current_shape:
            temp_long_list = [e[0] for e in sub_shape[0]]
            temp_lat_list = [e[1] for e in sub_shape[0]]
            temp_x_list = [mercator_projection_x(
                long) for long in temp_long_list]
            temp_y_list = [mercator_projection_y(
                lat) for lat in temp_lat_list]
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
        else:
            norm_max = (y_max - y_min) * 1.1
        x_offset = (1 - (x_max - x_min) / norm_max) * img_side / 2
        y_offset = (1 - (y_max - y_min) / norm_max) * img_side / 2

        for sub_shape in current_shape:
            long_list = [e[0] for e in sub_shape[0]]
            lat_list = [e[1] for e in sub_shape[0]]
            x_list = [mercator_projection_x(long) for long in long_list]
            y_list = [mercator_projection_y(lat) for lat in lat_list]

            x_list_norm = [(x - x_min) / norm_max
                           * img_side + x_offset for x in x_list]
            y_list_norm = [(y - y_min) / norm_max
                           * img_side + y_offset for y in y_list]
            coords_list = [(x_list_norm[i], img_side - y_list_norm[i])
                           for i in range(len(x_list))]
            current_image_draw.polygon(coords_list, fill=(
                255, 255, 255), outline=(255, 255, 255), width=10)
    # Save the image
    current_image.save(output_folder + current_ISO_code + ".png")
