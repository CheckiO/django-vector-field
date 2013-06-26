try:
    import cairosvg
except ImportError:
    cairosvg = None

from xml.etree import ElementTree
import re
from math import cos, sin, radians
import tools

COLORS_ATTR = {'fill': 'fill-opacity', 'stroke': 'stroke-opacity'}
DOCTYPE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
"""


class SvgImage():
    """
    The class for working with images in svg format.
    For parsing and changing using simple xml parsing.
    """

    def __init__(self, source=None, filename=None):
        """
        Create instance from file object or from text
        """
        if filename:
            with open(filename) as f:
                source = f.read()
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

    def get_svg_file(self, filename):
        """Save svg in file"""
        with open(filename, "w") as f:
            f.write(self.get_svg_text())

    def get_size(self):
        """self -> (float, float)
        Get size of image.
        Tuple of two int -- width and height
        """
        return (float(self.__root.attrib['width'].replace('px', '')),
                float(self.__root.attrib['height'].replace('px', '')))

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

    def scale(self, scale_width, scale_height):
        """
        self, float, float -> self
        Method for scale image.
        Width and height multiply at scale coefficient.
        """
        g = ElementTree.Element(
            "g",
            {"transform":
             "scale({0} {1})".format(scale_width, scale_height)})

        for el in list(self.__root):
            g.append(el)
            # self.__root.remove(el)
        self.__root.append(g)
        root_width, root_height = self.get_size()
        new_width = str(root_width * scale_width)
        new_height = str(root_width * scale_height)
        self.__root.set("width", new_width)
        self.__root.set("height", new_height)
        lower_root_keys = get_lower_keys(self.__root.attrib)
        self.__root.set(lower_root_keys.get("viewbox", "viewBox"),
                        "0, 0, {0}, {1}".format(new_width, new_height))

    def resize(self, width, height):
        """
        self, float, float -> self
        Method for resize image at new size.
        """
        root_width, root_height = self.get_size()
        self.scale(float(width) / root_width, float(height) / root_height)

    def rotate(self, angle, resize=False):
        """
        self, float, bool -> self
        Rotate the object at clockwise direction for angle in degree .
        """
        root_width, root_height = self.get_size()
        rad = radians(angle)
        new_width = cos(rad) * root_width + sin(rad) * root_height
        new_height = cos(rad) * root_height + sin(rad) * root_width
        print(locals())
        for el in list(self.__root):
            tr = el.attrib.get("transform", "")
            rotate = "rotate({0} {1} {2})".format(angle,
                                                  root_width / 2,
                                                  root_height / 2)
            translate = "translate({0}, {1})".format(
                (new_width - root_width) / 2,
                (new_height - root_height) / 2,

            )
            el.set(
                "transform",
                " ".join([tr, translate, rotate]))
        self.__root.set("width", str(int(new_width)))
        self.__root.set("height", str(int(new_height)))
        lower_root_keys = get_lower_keys(self.__root.attrib)
        self.__root.set(lower_root_keys.get("viewbox", "viewBox"),
                        "0, 0, {0}, {1}".format(new_width, new_height))

    def return_original(self):
        """
        self -> self
        Return object at original form.
        """
        self.__root = ElementTree.XML(self.__source)


def get_lower_keys(dictionary):
    """
    dict -> dict
    Get dictionary and create new dictionary with lowercase keys and keys from
    original dict as values.

    >>> get_lower_keys({"viewBox": 1, "VIEW": 2})
    {'viewbox': 'viewBox', 'view': 'VIEW'}
    """
    return dict([(k.lower(), k) for k in dictionary.keys()])