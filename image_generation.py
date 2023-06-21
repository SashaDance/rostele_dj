from PIL import Image, ImageDraw, ImageFont

IMAGE_WIDTH = 995
Y_WATERMARK = 1220
Y_TEXT = 810
Y_IMAGE = 32


def adjust_text(text):
    words = text.split()
    adjusted_text = ''
    current_line_len = 0
    # diving text into lines
    for word in words:
        if current_line_len + len(word) + 1 <= 50:
            adjusted_text += word + ' '
            current_line_len += len(word) + 1
        else:
            adjusted_text += '\n' + word + ' '
            current_line_len = len(word) + 1
    return adjusted_text


def adjust_images(image):
    image = Image.open(image)
    ratio = image.size[0] / image.size[1]
    image = image.resize((IMAGE_WIDTH, int(IMAGE_WIDTH / ratio)))
    return image


class PostImage:
    def __init__(self, text, image):
        background = Image.open("backgroung.jpg")

        self.new_image = Image.new("RGB", background.size, color="white")
        self.new_image.paste(background, (0, 0))

        # Pasting the images based on their number
        image = adjust_images(image)
        x = int((background.size[0] - image.size[0]) / 2)
        self.new_image.paste(image, (x, Y_IMAGE))

        draw = ImageDraw.Draw(self.new_image)

        text = adjust_text(text)
        watermark_text = '@numbers_game_dsj'
        font = ImageFont.truetype("arial.ttf", 36, encoding='utf-8')
        text_width, text_height = draw.textsize(text, font)
        watermark_text_width, watermark_text_height = draw.textsize(watermark_text, font)
        # Calculating text position and pasting it
        x_text = int((background.size[0] - text_width) / 2)
        x_watermark = int(((background.size[0] - watermark_text_width) / 2))
        draw.text((x_text, Y_TEXT), text, font=font, fill=(0, 0, 0))
        draw.text((x_watermark, Y_WATERMARK), watermark_text, font=font, fill=(200, 200, 200))

    def save(self, url):
        self.new_image.save(url)
