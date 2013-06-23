import unittest
from svg import SvgImage
from svg.tests import tools


class CreateSvgImageInstanceTestCase(unittest.TestCase):

    def test_from_file(self):
        f = tools.get_svg_file()
        icon = SvgImage(f)
        self.assertIsInstance(icon, SvgImage)

    def test_from_text(self):
        t = tools.get_svg_text()
        icon = SvgImage(t)
        self.assertIsInstance(icon, SvgImage)