def get_svg_file():
    try:
        f = open("./svg_icon.svg")
    except IOError:
        try:
            f = open("svg/tests/svg_icon.svg")
        except IOError:
            raise IOError("Cant open test svg file")
    return f


def get_svg_text():
    return get_svg_file().read()