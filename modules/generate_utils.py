import io
from PIL import Image, ImageDraw, ImageFont
from models.common.lat_lng_bounds import LatLngBounds
import requests
from modules.logging_utils import LoggingUtils
import qrcode
import textwrap3


class ImageGenerator():
    im_size = (1620, 2160)
    map_size = (1110, 1110)
    code_size = (600, 600)
    text_font = ImageFont.truetype("public/fonts/code_font.ttf", size=33)
    title_color = (176, 215, 63)
    title_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=170)
    name_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=75)
    black = (0, 0, 0)

    # horizontal paragraph aka spaghetti code
    @staticmethod
    def draw_multiple_line_text(image, text, font, text_color, text_start_height, vidth):
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

    # vertical paragraph aka spaghetti code 2.0
    def draw_multiple_line_text_y(text, font, text_color):
        im = Image.new(mode="RGBA", size=(1110, 1110), color=(255, 0, 255, 0))
        d = ImageDraw.Draw(im)

        lines = textwrap3.wrap(text, width=50)

        y_height = 0

        # dravs the lines
        for line in lines:
            line_height = font.getsize(line)[1]
            d.text((0, y_height), anchor="lt",
                   text=line, font=font, fill=text_color)
            y_height += line_height

        return im.rotate(-90).crop((690, 0, 1110, 1110))

    # ignorēt to kas tur augšā. te tas svarīgais
    @staticmethod
    def generate_image(location_name, code_img, map_img, name_surname, bottom_text, side_text):
        im = Image.new(mode="RGBA", size=ImageGenerator.im_size,
                       color=(255, 0, 255, 0))
        d = ImageDraw.Draw(im)

        # these drav the lines
        d.rectangle(
            (0, 255, ImageGenerator.im_size[0], 256), fill=ImageGenerator.black)
        d.rectangle((ImageGenerator.map_size[0]+45, 255,
                     ImageGenerator.map_size[0]+46, 300 + ImageGenerator.map_size[1]), fill=ImageGenerator.black)

        # these add images
        tobytes = b'\xbf\x8cd\xba\x7f\xe0\xf0\xb8t\xfe'

        offset = (1020, 1455)
        # te vajag zināt attēla dimensijas
        code_r = Image.frombytes('RGB', (474, 266), code_img, 'raw')
        code_r = code_r.resize(ImageGenerator.code_size)
        im.paste(code_r, offset)

        offset = (0, 300)
        map_r = Image.frombytes('RGB', (474, 266), code_img, 'raw')
        map_r = map_r.resize(ImageGenerator.map_size)
        im.paste(map_r, offset)

        # these lines add titles
        d.text((ImageGenerator.im_size[0]/2, 120), anchor="mt", align="center",
               text=location_name.upper(), font=ImageGenerator.title_font, fill=ImageGenerator.title_color)
        d.text((975, 1455), anchor="rt", align="center",
               text=name_surname.upper(), font=ImageGenerator.name_font, fill=ImageGenerator.black)

        # these ones add paragraphs
        ImageGenerator.draw_multiple_line_text(
            im, bottom_text, ImageGenerator.text_font, ImageGenerator.black, 2055, 45)
        im.paste(ImageGenerator.draw_multiple_line_text_y(
            side_text, ImageGenerator.text_font, ImageGenerator.black), (1200, 300))

        return im.tobytes()

    @staticmethod
    def generate_qr_img(text: str):
        qr_code_img = None
        try:
            qr_code_img = qrcode.make(text)
            print(type(qr_code_img))
        except Exception as e:
            LoggingUtils.log_exception(e)
        return qr_code_img

    @staticmethod
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

    @staticmethod
    def generate_normal_map_img():
        pass
