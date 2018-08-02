import sys

from shapify.palette.palette_builder import PaletteBuilder


if __name__ == '__main__':
    pic_name = 'test.png'
    if len(sys.argv) > 1:
        pic_name = sys.argv[1]

    pb = PaletteBuilder(None, filename=pic_name)

    palette = pb.get_new_palette()
    PaletteBuilder.show_palette(palette)
