import cairosvg


def save_png(svg_xml):
    """
    return png file content.
    It's use cairo module. Sometimes it can to fail with some unexpected
    attribute in svg file. For this it wrapped with try-except and return
    false or true if all ok.
    """
    svg_text = DOCTYPE + ElementTree.tostring(svg_xml)
    try:
        png = cairosvg.surface.PNGSurface.convert(svg_text)
        return png
    except Exception as er:
        return None, er
