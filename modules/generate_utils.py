from PIL import Image, ImageDraw, ImageFont

class image_generator():
    im_size = (500, 500)
    map_size = (im_size[0], 130)
    code_size = (130, 130)
    team_name = "Fungus Fanaticus"
    font = ImageFont.truetype("public/fonts/temp_font.ttf", size=40)

    #ja vajadzēs
    def render_gltf(gltf):
        pass
    
    def generate_image(code_image, map_img):
        im = Image.new(mode="RGBA", size=image_generator.im_size, color=(255,255,255, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((100,100,400,150), fill=(255,50,50))

        offset = (int((im.size[0]-image_generator.code_size[0])/2), 190)
        code_r = code_image.resize(image_generator.code_size)
        im.paste(code_r, offset)

        offset = (0, im.size[1]-image_generator.map_size[1])
        map_r = map_img.resize(image_generator.map_size)
        im.paste(map_r, offset)

        d.text((250,125),anchor="mm", align="center", text=image_generator.team_name, font=image_generator.font, fill=(255,255,255))

        return  im
