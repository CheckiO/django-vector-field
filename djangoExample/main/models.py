import sys
import os

from django.db import models

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ".."))

from svgField import SvgManipulationField, ManipulationVersion
from svgField.converters import PngConverter, SvgConverter
from svgField.manipulations import ScaleManipulation, RecolourManipulation, \
    RotateManipulation, ResizeManipulation, MultiRecolourManipulation


# Create your models here.
class Task(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    logo = SvgManipulationField(
        verbose_name="Logo",
        upload_to="logos/",
        null=True, blank=True,
        versions=(
            ManipulationVersion(
                name="small",
                manipulators=(
                    ScaleManipulation(scale=(2, 2)),
                    RotateManipulation(angle=30),
                    MultiRecolourManipulation(colors_translate={
                        "#FFFFFF": "#000000",
                        "#000000": "#FF0000"
                    })
                ),
                converter=PngConverter(),
                default_url="/media/123.png"
            ),
            ManipulationVersion(
                name="big_log",
                manipulators=(
                    ResizeManipulation(size=(1024, 1024)),
                    RecolourManipulation(from_color="#FFFFFF",
                                         to_color="#000000")
                ),
                converter=PngConverter(),
                default_url="/media/123.png"
            )
        )
    )