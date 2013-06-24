import unittest
from svg import SvgImage
from svg.tests import tools


class CreateSvgImageDataTestCase(unittest.TestCase):
    def setUp(self):
        self.icon = SvgImage(tools.get_svg_file())

    def test_get_size(self):
        expected = (128, 128)
        size = self.icon.get_size()
        self.assertEqual(size, expected)

    def test_get_elements_colors(self):
        expected = [
            {'color': "#737370",
             'type': "fill",
             'tag': "path",
             'id': ""},
            {'color': "#82D1F5",
             'type': "fill",
             'tag': "path",
             'id': ""},
            {'color': "#FFFFFF",
             'type': "fill",
             'tag': "path",
             'id': ""},
            {'color': "#EBEDED",
             'type': "fill",
             'tag': "path",
             'id': ""},
        ]
        elements_colors = self.icon.get_elements_colors()
        self.assertEqual(elements_colors, expected)