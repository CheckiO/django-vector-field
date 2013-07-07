
from xml.etree import ElementTree
import re
from math import cos, sin, radians

COLORS_ATTR = {'fill': 'fill-opacity', 'stroke': 'stroke-opacity'}
DOCTYPE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
"""


def read_svg(filename):
    with open(filename) as f:
        source = f.read()
    root = ElementTree.XML(source)
    try:
        lower_root_keys = get_lower_keys(root.attrib)
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



def get_size(svg_xml):
    """Element -> (float, float)
    Get size of image.
    Tuple of two int -- width and height
    """
    return (float(svg_xml.attrib['width'].replace('px', '')),
            float(svg_xml.attrib['height'].replace('px', '')))


def change_colors(svg_xml, colors_translate):
    """Element, dict -> self.
    Change colors inside Svg with translation dict.
    Translation colors dict: key is original color, value is which to set.
    Colors are strings.
    """
    from_colors = colors_translate.keys()
    for el in svg_xml.iter():
        for attr in COLORS_ATTR.keys():
            color = el.attrib.get(attr)
            if color in from_colors:
                el.set(attr, colors_translate[color])
    return svg_xml


def scale(svg_root, scale):
    """
    Element, [float, float] -> Element
    Method for scale image.
    Width and height multiply at scale coefficient.
    """
    scale_width, scale_height = scale
    g = ElementTree.Element(
        "g",
        {"transform": "scale({0} {1})".format(scale_width, scale_height)})
    for el in list(svg_root):
        g.append(el)
        svg_root.remove(el)
    svg_root.append(g)
    root_width, root_height = get_size(svg_root)
    new_width = str(root_width * scale_width)
    new_height = str(root_width * scale_height)
    svg_root.set("width", new_width)
    svg_root.set("height", new_height)
    lower_root_keys = get_lower_keys(svg_root.attrib)
    svg_root.set(lower_root_keys.get("viewbox", "viewBox"),
                 "0 0 {0} {1}".format(new_width, new_height))
    return svg_root


def rotate(svg_root, angle):
    """
    Element, float -> Element
    Rotate the object at clockwise direction for angle in degree .
    """
    root_width, root_height = get_size(svg_root)
    rad = radians(angle)
    new_width = cos(rad) * root_width + sin(rad) * root_height
    new_height = cos(rad) * root_height + sin(rad) * root_width

    rotate = "rotate({0} {1} {2})".format(angle,
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
    lower_root_keys = get_lower_keys(svg_root.attrib)
    svg_root.set(lower_root_keys.get("viewbox", "viewBox"),
                 "0 0 {0} {1}".format(new_width, new_height))
    return svg_root


def resize(svg_root, size):
    """
    Element, [float, float] -> Element
    Method for resize image at new size.
    """
    width, height = size
    root_width, root_height = get_size(svg_root)
    svg_root = scale(svg_root,
                     [float(width) / root_width, float(height) / root_height])
    return svg_root


def get_lower_keys(dictionary):
    """
    dict -> dict
    Get dictionary and create new dictionary with lowercase keys and keys from
    original dict as values.

    >>> get_lower_keys({"viewBox": 1, "VIEW": 2})
    {'viewbox': 'viewBox', 'view': 'VIEW'}
    """
    return dict([(k.lower(), k) for k in dictionary.keys()])