try:
    import cairosvg
except ImportError:
    cairosvg = None

from xml.etree import ElementTree
import re

COLORS_ATTR = {'fill': 'fill-opacity', 'stroke': 'stroke-opacity'}
DOCTYPE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
"""


class SvgImage():
    """
    The class for working with images in svg format.
    For parsing and changing using simple xml parsing.
    """

    def __init__(self, source):
        """
        Create instance from file object or from text
        """
        if type(source) == file:
            self.__source = source.read()
        elif type(source) in (str, unicode, basestring):
            self.__source = source
        else:
            raise TypeError("Must be file object or string")
        parsed_svg = ElementTree.XML(self.__source)
        self.__root = parsed_svg
        temp_re = re.match("^{.*?}", self.__root.tag)
        self.__xlmns = temp_re.group() if temp_re else {}
        ElementTree.register_namespace("", "http://www.w3.org/2000/svg")

    def get_svg_text(self):
        """Return text representation of svg"""
        return DOCTYPE + ElementTree.tostring(self.__root, method="html")

    def get_size(self):
        """self -> (int, int)
        Get size of image.
        Tuple of two int -- width and height
        """
        return (int(self.__root.attrib['width'].replace('px', '')),
                int(self.__root.attrib['height'].replace('px', '')))

    def get_elements_colors(self):
        """self -> list[dict,]
        Get elements' colors info.
        Return a list of dicts with color, type of color, tag and id of element.
        """
        res = []

        for el in self.__root.iter():
            for attr, attr_opacity in COLORS_ATTR.items():
                if (el.attrib.get(attr_opacity, '100') != '0' and
                        el.attrib.get(attr)):
                    res.append({'color': el.attrib[attr],
                                'type': attr,
                                'tag': el.tag.replace(self.__xlmns, ''),
                                'id': el.attrib.get('id', '')})
        return res

    def change_colors(self, colors_translate):
        """self, dict -> self.
        Change colors inside Svg with translation dict.
        Translation colors dict: key is original color, value is which to set.
        Colors are strings.
        """
        from_colors = colors_translate.keys()
        for el in self.__root.iter():
            for attr in COLORS_ATTR.keys():
                color = el.attrib.get(attr)
                if color in from_colors:
                    el.set(attr, colors_translate[color])

    def resize(self, scale_width, scale_height):
        """
        self, float, float -> self
        Method for resize image.
        Width and height multiply at scale cooficent.
        """
        root_width, root_height = self.get_size()
        self.__root.set("width", str(root_width * scale_width))
        self.__root.set("height", str(root_width * scale_height))