from svg import SvgImage
import tools

with open("./svg_icon.svg") as f:
    s = SvgImage(f)

# s.resize(1, 3)
# s.rotate(45)
s.scale(2, 3)

s.get_svg_file("result_svg.svg")