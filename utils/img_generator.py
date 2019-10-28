from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def get_image(text: str) -> bytes:
    fontsize = 1

    img_fraction = 0.70

    img_w, img_h = 150, 150

    img = Image.new('RGB', (img_w, img_h), color=(70, 70, 70))

    font_path = str(Path(__file__).resolve().parent.parent / 'fonts' / 'OpenSans-Regular.ttf')

    font = ImageFont.truetype(font_path, fontsize)
    while font.getsize(text)[0] < img_fraction * img.size[0]:
        fontsize += 1
        font = ImageFont.truetype(font_path, fontsize)

    font = ImageFont.truetype(font_path, fontsize)

    d = ImageDraw.Draw(img)
    font_w, font_h = d.textsize(text, font=font)

    d.text(((img_w - font_w) / 2, (img_h - font_h) / 2 - 30 if len(text) == 1 else 10), text, font=font)

    img.save('util.jpg')

    return open('util.jpg', 'rb').read()

