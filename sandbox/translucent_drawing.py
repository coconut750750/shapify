import sys

from PIL import Image, ImageDraw


if __name__ == '__main__':
    img1 = Image.new('RGBA', (255, 255))
    draw = ImageDraw.Draw(img1)
    draw.polygon([(1, 1), (20, 100), (100, 20)], fill=(255, 0, 0, 127))


    img2 = Image.new('RGBA', (255, 255))
    draw = ImageDraw.Draw(img2)
    draw.polygon([(1, 1), (20, 100), (100, 20)], fill=(0, 0, 255, 128))

    img = Image.alpha_composite(img1, img2)
    img.show()
