import io
from PIL.TiffImagePlugin import TiffImageFile
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.pil import PilImage
from models.common.design_bottom_text import DesignBottomText
from models.common.lat_lng_bounds import LatLngBounds
import requests
from modules.logging_utils import LoggingUtils
import qrcode
import json
from modules.consts import PATH_PUBLIC

import numpy as np
import textwrap3
import cv2


class ImageGenerator():
    im_size = (1620, 2160)
    map_size = (1110, 1110)
    code_size = (600, 600)
    text_font = ImageFont.truetype("public/fonts/code_font.ttf", size=33)
    title_color = (176, 215, 63)
    title_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=170)
    name_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=75)
    black = (0, 0, 0)
    lines = cv2.imread('public/images/lines.png', flags=cv2.IMREAD_UNCHANGED)

    def generate_distorted_map(h_map):
        result = None
        try:
            #b_vidth, b_height = h_map.size
            #h_map_bytes = h_map.tobytes()
            #background = np.fromstring(h_map_bytes, dtype=np.uint8)
            #background = background.reshape(
            #    (b_height,b_vidth, 4))
            background = cv2.imread(h_map)
            background = cv2.cvtColor(background, cv2.COLOR_RGBA2GRAY)
            cv2.imwrite("Test_background.png",background)

            background = cv2.resize(background, (800, 800),
                                    interpolation=cv2.INTER_AREA)
            background = cv2.medianBlur(background, 21)
            rows, cols = (800, 800)

            result = np.zeros((800, 800, 4), dtype=np.uint8)
            minVal, maxVal = cv2.minMaxLoc(background)[:2]
            l_dist= (maxVal-minVal)

            # cycles trough each pixel
            for i in range(rows):
                if not i%40:
                    for j in range(cols):
                        offset_y = int((background[i, j]-minVal)*(40/l_dist))
                        if offset_y < int(l_dist/5):
                            offset_y = int(l_dist/5)
                        # shifts the pixels upvards
                        if i+offset_y < rows:
                            for line in range(0,5):
                                result[i+offset_y-line, j] = [63,215,176,255]
                        else:
                            result[i, j][0] = 0

            result = cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA)
            result = Image.fromarray(result)
        except Exception as e:
            LoggingUtils.log_exception(e)
        return result

    # horizontal paragraph aka spaghetti code
    @staticmethod
    def draw_multiple_line_text(image, text, font, text_color, text_start_height, vidth):
        try:
            draw = ImageDraw.Draw(image)

            lines = textwrap3.wrap(text, width=vidth)

            # calculates vhere to start vriting
            y_height = 0
            for line in lines:
                line_height = font.getsize(line)[1]
                y_height += line_height
            y_text = text_start_height - y_height

            # yeah and this one just dravs the lines
            for line in lines:
                line_height = font.getsize(line)[1]
                draw.text((975, y_text), anchor="rt",
                          text=line, font=font, fill=text_color)
                y_text += line_height
        except Exception as e:
            LoggingUtils.log_exception(e)

    # vertical paragraph aka spaghetti code 2.0
    def draw_multiple_line_text_y(text, font, text_color):
        result = None
        try:
            result = Image.new(mode="RGBA", size=(
                1110, 1110), color=(255, 0, 255, 0))
            d = ImageDraw.Draw(result)

            lines = textwrap3.wrap(text, width=50)

            y_height = 0

            # dravs the lines
            for line in lines:
                line_height = font.getsize(line)[1]
                d.text((0, y_height), anchor="lt",
                       text=line, font=font, fill=text_color)
                y_height += line_height
        except Exception as e:
            LoggingUtils.log_exception(e)
        return result.rotate(-90).crop((690, 0, 1110, 1110))

    @staticmethod
    def get_bottom_text() -> DesignBottomText:
        result = None
        try:
            result = DesignBottomText()
            f = open(f'{PATH_PUBLIC}/edition/edition.json',)
            data = json.load(f)
            result.title = data['title']
            result.description = data['description']
        except Exception as e:
            LoggingUtils.log_exception(e)
        return result

    # ignorēt to kas tur augšā. te tas svarīgais
    @staticmethod
    def generate_design_image(location_name, qr_code_img, map_img: PilImage, side_text, bottom_title, bottom_desc) -> PilImage:
        result = None
        try:
            result = Image.new(mode="RGBA", size=ImageGenerator.im_size,
                               color=(255, 0, 255, 0))
            d = ImageDraw.Draw(result)

            # these drav the lines
            d.rectangle(
                (0, 255, ImageGenerator.im_size[0], 256), fill=ImageGenerator.black)
            d.rectangle((ImageGenerator.map_size[0]+45, 255,
                        ImageGenerator.map_size[0]+46, 300 + ImageGenerator.map_size[1]), fill=ImageGenerator.black)

            offset = (1020, 1455)
            # te vajag zināt attēla dimensijas
            code_r = qr_code_img.resize(ImageGenerator.code_size)
            result.paste(code_r, offset)

            offset = (0, 300)
            map_r = map_img.resize(ImageGenerator.map_size)
            result.paste(map_r, offset)

            # Add titles
            d.text((ImageGenerator.im_size[0]/2, 215), anchor="mb", align="left",
                   text=location_name.upper(), font=ImageGenerator.title_font, fill=ImageGenerator.title_color)
            d.text((975, 1455), anchor="rt", align="center",
                   text=bottom_title.upper(), font=ImageGenerator.name_font, fill=ImageGenerator.black)

            # these ones add paragraphs
            ImageGenerator.draw_multiple_line_text(
                result, bottom_desc, ImageGenerator.text_font, ImageGenerator.black, 2055, 45)
            result.paste(ImageGenerator.draw_multiple_line_text_y(
                side_text, ImageGenerator.text_font, ImageGenerator.black), (1200, 300))
        except Exception as e:
            LoggingUtils.log_exception(e)
        print(type(result), 'design image')
        return result

    @staticmethod
    def generate_qr_img(text: str):
        qr_code_img = None
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=50,
                border=0,
            )
            qr.add_data(text)
            qr.make(fit=True)
            qr_code_img = qr.make_image(fill_color="black", back_color="white")
        except Exception as e:
            LoggingUtils.log_exception(e)
        print(type(qr_code_img), 'qr_image')
        return qr_code_img

    @ staticmethod
    def generate_elevation_map_img(bounds: LatLngBounds):
        elevation_map_img = None
        try:
            url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={bounds.south}&north={bounds.north}&west={bounds.west}&east={bounds.east}'
            res = requests.get(url)
            stream = io.BytesIO(res.content)
            elevation_map_img = Image.open(stream)
            print(type(elevation_map_img))
        except Exception as e:
            LoggingUtils.log_exception(e)
        return elevation_map_img

    @ staticmethod
    def generate_normal_map_img(elevation_map: TiffImageFile):
        pass
