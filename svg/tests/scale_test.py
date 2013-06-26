import unittest
from svg import SvgImage
from svg.tests import tools


class ResizeTestCase(unittest.TestCase):
    def setUp(self):
        self.icon = SvgImage(tools.get_svg_file())

    def test_scale_twice(self):
        self.icon.scale(2, 2)
        expected = (256, 256)
        size = self.icon.get_size()
        self.assertEqual(expected, size)