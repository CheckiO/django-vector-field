# import cairosvg
from xml.etree import ElementTree
import re


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
        colors_attrib = [('fill', 'fill-opacity'), ('stroke', 'stroke-opacity')]
        for el in self.__elements:
            for attr in colors_attrib:
                if el.attrib.get(attr[1], '100') != '0' and el.attrib.get(attr[0]):
                    res.append({'color': el.attrib[attr[0]],
                                'type': attr[0],
                                'tag': el.tag.replace(self.__xlmns, ''),
                                'id': el.attrib.get('id', '')})
        return res

