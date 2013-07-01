from django.db import models
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ".."))

from svgManipulationField import SvgManipulationField
from svgManipulationField import save_png, scale, rotate


# Create your models here.
class TestM(models.Model):
    name = models.CharField(max_length=30)
    image = SvgManipulationField(
        verbose_name="Logo",
        upload_to="media/",
        versions=[
            {"name": "small_png",
             "manipulations": [(scale, [2, 2]), (rotate, 30)],
             "converter": save_png,
             "extension": "png",
             "default_url": "http://www.w3.org/Icons/w3c_home"}
        ],
        null=True, blank=True
    )