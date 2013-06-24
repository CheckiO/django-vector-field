import unittest
from svg import SvgImage
from svg.tests import tools


class ChangeColorsTestCase(unittest.TestCase):
    def setUp(self):
        self.icon = SvgImage(tools.get_svg_file())

    def check_colors(self, colors_translation, expected_colors):
        self.icon.change_colors(colors_translation)
        elements_colors = self.icon.get_elements_colors()
        colors = [d["color"] for d in elements_colors]
        self.assertEqual(colors, expected_colors)

    def test_change_colors_all(self):
        colors_translation = {
            "#737370": "#9D9E9E",
            "#82D1F5": "#294270",
            "#FFFFFF": "#000000",
            "#EBEDED": "#737370"
        }
        expected_colors = [
            "#9D9E9E",
            "#294270",
            "#000000",
            "#737370"
        ]
        self.check_colors(colors_translation, expected_colors)

    def test_change_colors_empty(self):
        colors_translation = {}
        expected_colors = [
            "#737370",
            "#82D1F5",
            "#FFFFFF",
            "#EBEDED",
        ]
        self.check_colors(colors_translation, expected_colors)

    def test_change_colors_absent(self):
        colors_translation = {
            "#000000": "#111111"
        }
        expected_colors = [
            "#737370",
            "#82D1F5",
            "#FFFFFF",
            "#EBEDED",
            ]
        self.check_colors(colors_translation, expected_colors)