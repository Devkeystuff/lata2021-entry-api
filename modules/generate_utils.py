from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap3, cv2

class ImageGenerator():
    im_size = (1620, 2160)
    map_size = (1110, 1110)
    code_size = (600, 600)
    text_font = ImageFont.truetype("public/fonts/code_font.ttf", size=33)
    title_color = (176, 215, 63)
    title_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=170)
    name_font = ImageFont.truetype("public/fonts/ralevay_font.ttf", size=75)
    black = (0,0,0)
    lines = cv2.imread('public/images/lines.png', flags=cv2.IMREAD_UNCHANGED)

    #plottvist this one dravs maps
    def DravMap(h_map, img):
        background = np.fromstring(h_map, dtype=np.uint8)
        background = background.reshape((640,640,3))  #te vajag zināt height map izmēru un vai tas ir RGB/RGBA
        background = cv2.cvtColor(background, cv2.COLOR_RGBA2GRAY)
        img = cv2.resize(img, (810,810), interpolation = cv2.INTER_AREA)
        background = cv2.resize(background, (810,810), interpolation = cv2.INTER_AREA)
        background = cv2.medianBlur(background, 21)
        rows, cols = (810,810)

        img_output = np.zeros((810,810,4), dtype=img.dtype)

        #cycles trough each pixel
        for i in range(rows):
            for j in range(cols):
        
                #gets rid of the darkest and brightest pixels
                if background[i,j]> 240:
                    background[i,j] = 240
                elif background[i,j]< 15:
                    background[i,j] = 15    

                offset_y = int((background[i,j]-15)*0.35)
                #shifts the pixels upvards
                if i+offset_y < rows:
                    img_output[i,j] = img[(i+offset_y)%rows,j]
                else:
                    img_output[i,j][0] = 0

        img_output = cv2.cvtColor(img_output, cv2.COLOR_BGRA2RGBA)
        return img_output.tobytes()

    #horizontal paragraph aka spaghetti code
    def draw_multiple_line_text(image, text, font, text_color, text_start_height, vidth):
        draw = ImageDraw.Draw(image)

        lines = textwrap3.wrap(text, width=vidth)

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

        lines = textwrap3.wrap(text, width=50)

        y_height =0
        
        #dravs the lines
        for line in lines:
            line_height = font.getsize(line)[1]
            d.text((0, y_height),anchor="lt", text=line, font=font, fill=text_color)
            y_height += line_height

        return  im.rotate(-90).crop((690,0,1110,1110))

    #ignorēt to kas tur augšā. te tas svarīgais
    def generate_image(location_name, code_img, map_img, bottom_text, side_text):
        im = Image.new(mode="RGBA", size=ImageGenerator.im_size, color=(255,0,255,0))
        d = ImageDraw.Draw(im)

        #these drav the lines
        d.rectangle((0,255,ImageGenerator.im_size[0],256), fill=ImageGenerator.black)
        d.rectangle((ImageGenerator.map_size[0]+45,255,
        ImageGenerator.map_size[0]+46,300 + ImageGenerator.map_size[1]), fill=ImageGenerator.black)

        #these add images        
        offset = (1020,1455)
        code_r = Image.frombytes('RGB', (1200,1200), code_img, 'raw') #te vajag zināt qr_coda izmēru
        code_r = code_r.resize(ImageGenerator.code_size)
        im.paste(code_r, offset)

        offset = (0, 300)
        map_r = Image.frombytes('RGBA', (810,810), ImageGenerator.DravMap(map_img, ImageGenerator.lines), 'raw')
        map_r = map_r.resize(ImageGenerator.map_size)
        im.paste(map_r, offset)

        #these lines add titles
        d.text((ImageGenerator.im_size[0]/2,215),anchor="mb", align="center",
        text=location_name.upper(), font=ImageGenerator.title_font, fill=ImageGenerator.title_color)
        d.text((975,1455),anchor="rt", align="center",
        text="HUMBOLDT.", font=ImageGenerator.name_font, fill=ImageGenerator.black)

        #these ones add paragraphs
        ImageGenerator.draw_multiple_line_text(im, bottom_text, ImageGenerator.text_font, ImageGenerator.black, 2055, 45)
        im.paste(ImageGenerator.draw_multiple_line_text_y(side_text, ImageGenerator.text_font, ImageGenerator.black), (1200, 300))

        return  im.tobytes()
