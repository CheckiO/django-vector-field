from svgManipulationField import SvgManipulationField
from converters import SvgConverter
import os
from manipulations import Manipulation


class ManipulationVersion():
    def __init__(self, name, manipulators=(), converter=SvgConverter(), default_url=""):
        self.name = name
        self.manipulators = manipulators
        self.converter = converter
        self.default_url = default_url

    def write_version_file(self, base_path):
        dir_path, filename = os.path.split(base_path)
        base_name = filename.rsplit(".", 1)[0]
        version_dir = os.path.join(dir_path, self.name)
        version_filename = os.path.join(
            version_dir, ".".join([base_name, self.converter.extension]))
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)
        svg_root = Manipulation.read_svg(base_path)
        for m in self.manipulators:
            svg_root = m.manipulate(svg_root)
        self.converter.convert(svg_root, write_to=version_filename)