import cairosvg
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
        self.__root = parsed_svg.getroot()
        self.__elements = self.__root.iter()
        temp_re = re.match("^{.*?}", self.__root.tag)
        self.__xlmns = temp_re.group() if temp_re else {}
