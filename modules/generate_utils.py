import io
from PIL.TiffImagePlugin import TiffImageFile
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.pil import PilImage
from models.common.design_bottom_text import DesignBottomText
from models.common.lat_lng_bounds import LatLngBounds
import requests
from modules.logging_utils import LoggingUtils
import qrcode
import textwrap3
import json

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

    def generate_distorted_map(h_map: bytes, img):
        result = None
        try:
            background = np.fromstring(h_map, dtype=np.uint8)
            # te vajag zināt height map izmēru un vai tas ir RGB/RGBA
            background = background.reshape((640, 640, 3))
            background = cv2.cvtColor(background, cv2.COLOR_RGBA2GRAY)
            img = cv2.resize(img, (810, 810), interpolation=cv2.INTER_AREA)
            background = cv2.resize(background, (810, 810),
                                    interpolation=cv2.INTER_AREA)
            background = cv2.medianBlur(background, 21)
            rows, cols = (810, 810)

            result = np.zeros((810, 810, 4), dtype=img.dtype)

            # cycles trough each pixel
            for i in range(rows):
                for j in range(cols):

                    # gets rid of the darkest and brightest pixels
                    if background[i, j] > 240:
                        background[i, j] = 240
                    elif background[i, j] < 15:
                        background[i, j] = 15

                    offset_y = int((background[i, j]-15)*0.35)
                    # shifts the pixels upvards
                    if i+offset_y < rows:
                        result[i, j] = img[(i+offset_y) % rows, j]
                    else:
                        result[i, j][0] = 0

            result = cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA)
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
            f = json.load('public/edition/edition.json')
            result.title = f['title']
            result.description = f['description']
        except Exception as e:
            LoggingUtils.log_exception(e)
        return result

    # ignorēt to kas tur augšā. te tas svarīgais
    @staticmethod
    def generate_design_image(location_name, qr_code_img, map_img: PilImage, side_text) -> PilImage:
        result = None
        try:
            bottom_section = ImageGenerator.get_bottom_text()

            result = Image.new(mode="RGBA", size=ImageGenerator.im_size,
                               color=(255, 0, 255, 0))
            d = ImageDraw.Draw(result)

            # these drav the lines
            d.rectangle(
                (0, 255, ImageGenerator.im_size[0], 256), fill=ImageGenerator.black)
            d.rectangle((ImageGenerator.map_size[0]+45, 255,
                        ImageGenerator.map_size[0]+46, 300 + ImageGenerator.map_size[1]), fill=ImageGenerator.black)

            # Add images
            tobytes = b'\xbf\x8cd\xba\x7f\xe0\xf0\xb8t\xfe'

            offset = (1020, 1455)
            # te vajag zināt attēla dimensijas
            code_r = Image.frombytes('RGB', (474, 266), qr_code_img, 'raw')
            code_r = code_r.resize(ImageGenerator.code_size)
            result.paste(code_r, offset)

            offset = (0, 300)
            map_r = Image.frombytes('RGBA', (810, 810), ImageGenerator.DravMap(
                map_img, ImageGenerator.lines), 'raw')
            map_r = map_r.resize(ImageGenerator.map_size)
            result.paste(map_r, offset)

            # Add titles
            d.text((ImageGenerator.im_size[0]/2, 120), anchor="mt", align="left",
                   text=location_name.upper(), font=ImageGenerator.title_font, fill=ImageGenerator.title_color)
            d.text((975, 1455), anchor="rt", align="center",
                   text=bottom_section.title.upper(), font=ImageGenerator.name_font, fill=ImageGenerator.black)

            # these ones add paragraphs
            ImageGenerator.draw_multiple_line_text(
                result, bottom_section.description, ImageGenerator.text_font, ImageGenerator.black, 2055, 45)
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
