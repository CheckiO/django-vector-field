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


class CreateSvgImageDataTestCase(unittest.TestCase):

    def setUp(self):
        self.icon = SvgImage(tools.get_svg_file())
        self.root = self.icon._SvgImage__root
        self.xmlns = self.icon._SvgImage__xlmns

    def test_root(self):
        self.assertEqual(self.root.tag, '{http://www.w3.org/2000/svg}svg')

    def test_xmlns(self):
        self.assertEqual(self.xmlns, '{http://www.w3.org/2000/svg}')