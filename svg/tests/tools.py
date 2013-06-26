import doctest

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

def get_lower_keys(dictionary):
    """
    dict -> dict
    Get dictionary and create new dictionary with lowercase keys and keys from
    original dict as values.

    >>> get_lower_keys({"viewBox": 1, "VIEW": 2})
    {'viewbox': 'viewBox', 'view': 'VIEW'}
    """
    return dict([(k.lower(), k) for k in dictionary.keys()])

if __name__ == '__main__':
    doctest.testmod()