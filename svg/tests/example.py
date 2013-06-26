from svg import SvgImage
import tools

with open("./svg_icon.svg") as f:
    s = SvgImage(f)

s.resize(200, 300)
s.save_svg_file("result_svg_resized.svg")

s.return_original()
s.rotate(90)
s.save_svg_file("result_svg_right.svg")

s.return_original()
s.rotate(45)
s.save_svg_file("result_svg_45.svg")

s.return_original()
s.rotate(30)
s.save_svg_file("result_svg_30.svg")

s.return_original()
s.scale(2, 1)
s.rotate(30)
s.save_svg_file("result_svg_s30.svg")
result_save = s.save_png_file("result_png_s30.png")
# s.scale(2, 3)

s.return_original()
result_save = s.save_png_file("result_png.png")