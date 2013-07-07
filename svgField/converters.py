from xml.etree import ElementTree
import cairosvg

DOCTYPE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
"""


class Converter():
    def __init__(self):
        pass

    @property
    def extension(self):
        return ""

    def convert(self, svg_xml, write_to=None):
        raise NotImplementedError


class PngConverter(Converter):
    @property
    def extension(self):
        return "png"

    def convert(self, svg_xml, write_to=None):
        svg_text = DOCTYPE + ElementTree.tostring(svg_xml)
        #PNGSurface crush at every error in svg
        try:
            png = cairosvg.surface.PNGSurface.convert(svg_text, write_to=write_to)
            return png
        except Exception:
            return None


class SvgConverter(Converter):
    @property
    def extension(self):
        return "svg"

    def convert(self, svg_xml, write_to=None):
        svg_txt = DOCTYPE + ElementTree.tostring(svg_xml)
        svg = cairosvg.surface.SVGSurface.convert(svg_txt, write_to=write_to)
        return svg
