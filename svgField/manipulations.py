from xml.etree import ElementTree
import re
from math import cos, sin, radians

COLORS_ATTR = {'fill': 'fill-opacity', 'stroke': 'stroke-opacity'}


class Manipulation():
    @classmethod
    def read_svg(cls, filename):
        with open(filename) as f:
            source = f.read()
        root = ElementTree.XML(source)
        try:
            lower_root_keys = Manipulation.get_lower_keys(root.attrib)
            viewbox_key = lower_root_keys.get("viewbox", "viewBox")
            viewbox = root.attrib.get(viewbox_key, None)
            if viewbox:
                viewbox_values = re.findall(
                    r"(\d+)[, ]+(\d+)[, ]+(\d+)[, ]+(\d+)",
                    viewbox)
                root.set(viewbox_key,
                         "{0} {1} {2} {3}".format(*viewbox_values[0]))
        except Exception:
            pass
        return root

    @classmethod
    def get_size(cls, svg_root):
        """Element -> (float, float)
        Get size of image.
        Tuple of two int -- width and height
        """
        return (float(svg_root.attrib['width'].replace('px', '')),
                float(svg_root.attrib['height'].replace('px', '')))

    @classmethod
    def get_lower_keys(cls, dictionary):
        """
        dict -> dict
        Get dictionary and create new dictionary with lowercase keys and keys from
        original dict as values.

        >>> Manipulation.get_lower_keys({"viewBox": 1, "VIEW": 2})
        {'viewbox': 'viewBox', 'view': 'VIEW'}
        """
        return dict([(k.lower(), k) for k in dictionary.keys()])

    def manipulate(self, svg_root):
        raise NotImplementedError


class MultiRecolourManipulation(Manipulation):
    def __init__(self, colors_translate):
        self.colors_translate = colors_translate

    def manipulate(self, svg_root):
        from_colors = self.colors_translate.keys()
        for el in svg_root.iter():
            for attr in COLORS_ATTR.keys():
                color = el.attrib.get(attr)
                if color in from_colors:
                    el.set(attr, self.colors_translate[color])
        return svg_root


class RecolourManipulation(Manipulation):
    def __init__(self, from_color, to_color):
        self.from_color = from_color
        self.to_color = to_color

    def manipulate(self, svg_root):
        return MultiRecolourManipulation({
            self.from_color: self.to_color}).manipulate(svg_root)


class ScaleManipulation(Manipulation):
    def __init__(self, scale=(1, 1)):
        if type(scale) is int or type(scale) is float:
            self.scale = (scale, scale)
        else:
            self.scale = scale

    def manipulate(self, svg_root):

        scale_width, scale_height = self.scale
        g = ElementTree.Element(
            "g",
            {"transform": "scale({0} {1})".format(scale_width, scale_height)})
        for el in list(svg_root):
            g.append(el)
            svg_root.remove(el)
        svg_root.append(g)
        root_width, root_height = self.get_size(svg_root)
        new_width = str(root_width * scale_width)
        new_height = str(root_width * scale_height)
        svg_root.set("width", new_width)
        svg_root.set("height", new_height)
        lower_root_keys = self.get_lower_keys(svg_root.attrib)
        svg_root.set(lower_root_keys.get("viewbox", "viewBox"),
                     "0 0 {0} {1}".format(new_width, new_height))
        return svg_root


class RotateManipulation(Manipulation):
    def __init__(self, angle):
        self.angle = angle

    def manipulate(self, svg_root):
        """
        Element, float -> Element
        Rotate the object at clockwise direction for angle in degree .
        """
        root_width, root_height = self.get_size(svg_root)
        rad = radians(self.angle)
        new_width = cos(rad) * root_width + sin(rad) * root_height
        new_height = cos(rad) * root_height + sin(rad) * root_width

        rotate = "rotate({0} {1} {2})".format(self.angle,
                                              root_width / 2,
                                              root_height / 2)
        translate = "translate({0}, {1})".format(
            (new_width - root_width) / 2,
            (new_height - root_height) / 2,

        )

        g = ElementTree.Element(
            "g",
            {"transform": " ".join([translate, rotate])})

        for el in list(svg_root):
            g.append(el)
            svg_root.remove(el)
        svg_root.append(g)

        svg_root.set("width", str(int(new_width)))
        svg_root.set("height", str(int(new_height)))
        lower_root_keys = self.get_lower_keys(svg_root.attrib)
        svg_root.set(lower_root_keys.get("viewbox", "viewBox"),
                     "0 0 {0} {1}".format(new_width, new_height))
        return svg_root


class ResizeManipulation(Manipulation):
    def __init__(self, size):
        self.size = size

    def manipulate(self, svg_root):
        """
        Element, [float, float] -> Element
        Method for resize image at new size.
        """
        width, height = self.size
        root_width, root_height = Manipulation.get_size(svg_root)
        w_scale = float(width) / root_width
        h_scale = float(height) / root_height
        return ScaleManipulation((w_scale, h_scale)).manipulate(svg_root)

