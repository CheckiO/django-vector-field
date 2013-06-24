# import cairosvg
from xml.etree import ElementTree
import re

COLORS_ATTR = {'fill': 'fill-opacity', 'stroke': 'stroke-opacity'}

class SvgImage():
    """
    The class for working with images in svg format.
    For parsing and changing using simple xml parsing.
    """

    def __init__(self, source):
        if type(source) == file:
            self.__source = source.read()
        elif type(source) in (str, unicode, basestring):
            self.__source = source
        else:
            raise TypeError("Must be file object or string")
        parsed_svg = ElementTree.fromstring(self.__source)
        self.__root = parsed_svg
        self.__elements = self.__root.iter()
        temp_re = re.match("^{.*?}", self.__root.tag)
        self.__xlmns = temp_re.group() if temp_re else {}

    def get_svg_text(self):
        """Return text representation of svg"""
        return self.__source

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

        for el in self.__elements:
            for attr, attr_opacity in COLORS_ATTR.items():
                if (el.attrib.get(attr_opacity, '100') != '0' and
                        el.attrib.get(attr)):
                    res.append({'color': el.attrib[attr],
                                'type': attr,
                                'tag': el.tag.replace(self.__xlmns, ''),
                                'id': el.attrib.get('id', '')})
        return res
