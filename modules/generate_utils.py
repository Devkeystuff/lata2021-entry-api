from PIL import Image, ImageDraw, ImageFont
import textwrap

class image_generator():
    im_size = (1620, 2160)
    map_size = (1110, 1110)
    code_size = (600, 600)
    text_font = ImageFont.truetype("public/fonts/code_font.ttf", size=33)
    title_color = (176, 215, 63)
    title_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=130)
    name_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=75)
    black = (0,0,0)

    #horizontal paragraph aka spaghetti code
    def draw_multiple_line_text(image, text, font, text_color, text_start_height, vidth):
        draw = ImageDraw.Draw(image)

        lines = textwrap.wrap(text, width=vidth)

        #calculates vhere to start vriting
        y_height =0
        for line in lines:
            line_height = font.getsize(line)[1]
            y_height += line_height
        y_text = text_start_height -y_height
        
        #yeah and this one just dravs the lines
        for line in lines:
            line_height = font.getsize(line)[1]
            draw.text((975, y_text),anchor="rt", text=line, font=font, fill=text_color)
            y_text += line_height
    
    #vertical paragraph aka spaghetti code 2.0
    def draw_multiple_line_text_y(text, font, text_color):
        im = Image.new(mode="RGBA", size=(1110,1110), color=(255,0,255,0))
        d = ImageDraw.Draw(im)

        lines = textwrap.wrap(text, width=50)

        y_height =0
        
        #dravs the lines
        for line in lines:
            line_height = font.getsize(line)[1]
            d.text((0, y_height),anchor="lt", text=line, font=font, fill=text_color)
            y_height += line_height

        return  im.rotate(-90).crop((690,0,1110,1110))

    #ignorēt to kas tur augšā. te tas svarīgais
    def generate_image(location_name, code_image, map_img, name_surname, bottom_text, side_text):
        im = Image.new(mode="RGBA", size=image_generator.im_size, color=(255,0,255,0))
        d = ImageDraw.Draw(im)

        #these drav the lines
        d.rectangle((0,255,image_generator.im_size[0],256), fill=image_generator.black)
        d.rectangle((image_generator.map_size[0]+45,255,
        image_generator.map_size[0]+46,300 + image_generator.map_size[1]), fill=image_generator.black)

        #these add images
        offset = (1020,1455)
        code_r = code_image.resize(image_generator.code_size)
        im.paste(code_r, offset)

        offset = (0, 300)
        map_r = map_img.resize(image_generator.map_size)
        im.paste(map_r, offset)

        #these lines add titles
        d.text((image_generator.im_size[0]/2,120),anchor="mt", align="center",
        text=location_name.upper(), font=image_generator.title_font, fill=image_generator.title_color)
        d.text((975,1455),anchor="rt", align="center",
        text=name_surname.upper(), font=image_generator.name_font, fill=image_generator.black)

        #these ones add paragraphs
        image_generator.draw_multiple_line_text(im, bottom_text, image_generator.text_font, image_generator.black, 2055, 45)
        im.paste(image_generator.draw_multiple_line_text_y(side_text, image_generator.text_font, image_generator.black), (1200, 300))

        return  im
