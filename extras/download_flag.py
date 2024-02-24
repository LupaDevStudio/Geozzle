import requests
import shutil

# response = requests.get(
#     url="https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg",
#     timeout=5)

# print(response)
# data = response.text
# end_mark = data.find("Original file</a>") + len("Original file</a>")
# print(end_mark)
# cut_data = data[:end_mark]
# # print(cut_data)
# begin_mark = cut_data.rfind("<a")
# extracted_data = data[begin_mark:end_mark]
# print(extracted_data)

# segments = extracted_data.split(" ")
# for segment in segments:
#     if "href" in segment:
#         result = segment[:-1].replace('href="', "")
#         break

# print(result)

# name = result.split("/")[-1]

# png_url = result + f"/512px-{name}.png"

# png_url = png_url.replace("https://upload.wikimedia.org/wikipedia/commons/",
#                           "https://upload.wikimedia.org/wikipedia/commons/thumb/")

# print(png_url)


# url = png_url
# response = requests.get(url, stream=True)
# with open('out.png', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
# del response


def download_png_from_svg_url(svg_url):
    try:
        response = requests.get(
            url=svg_url,
            timeout=5)
        data = response.text
        # print(data)
        end_mark = data.find("Original file</a>") + len("Original file</a>")
        cut_data = data[:end_mark]
        begin_mark = cut_data.rfind("<a")
        # print(cut_data)
        extracted_data = data[begin_mark:end_mark]
        # print(extracted_data)

        segments = extracted_data.split(" ")
        for segment in segments:
            if "href" in segment:
                result = segment[:-1].replace('href="', "")
                break

        name = result.split("/")[-1]

        png_url = result + f"/512px-{name}.png"

        png_url = png_url.replace("https://upload.wikimedia.org/wikipedia/commons/",
                                  "https://upload.wikimedia.org/wikipedia/commons/thumb/")
        # print(png_url)

        url = png_url

        headers = {
            'User-Agent': 'Geozzle/1.0 (https://lupadevstudio.com; lupa.dev.studio@gmail.com) python-requests/2.28.2'}

        response = requests.get(url, headers=headers, stream=True)
        # print(response.status_code)
        # print(response.text)
        with open('out.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        # del response
        return True
    except:
        print("No connection")
        return False


download_png_from_svg_url(
    "https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg")
