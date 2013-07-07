
from django.db.models import signals
from django.db import models
from django.db.models.fields.files import FieldFile
import os

class SvgManipulationField(models.FileField):

    def __init__(self, verbose_name=None, name=None, upload_to=None,
                 versions=None, **kwargs):
        self.versions = versions
        super(SvgManipulationField, self).__init__(verbose_name, name,
                                                   upload_to, **kwargs)

    def get_paths(self, value):
        full_path = value.path
        return os.path.split(full_path)

    def get_db_prep_save(self, value, connection):
        if value:
            dir_path, filename = self.get_paths(value)
            try:
                base_name, extension = filename.rsplit(".", 1)
            except ValueError:
                raise ValueError("Must be SVG file.")
            for version in self.versions:
                version_dir = os.path.join(dir_path, version["name"])
                if not os.path.exists(version_dir):
                    os.makedirs(version_dir)
                component = read_svg(value.path)
                try:
                    for manipulation_func, arguments in version["manipulations"]:
                        component = manipulation_func(component, arguments)
                except ValueError:
                    raise TypeError(
                        "Each manipulation must be a two-element tuple.")
                result = version["converter"](component)

                if result:
                    version_filename = os.path.join(
                        version_dir, ".".join([base_name, version["extension"]]))
                    with open(version_filename, "w") as version_f:
                        version_f.write(result)
                else:
                    raise TypeError(
                        "Problem with convertor: {0}".format(result[1]))
        return self.get_prep_value(value)

    def __add_attributes(self, instance, **kwargs):

        f_file = getattr(instance, self.name)

        for v in self.versions:
            if f_file:
                base_url, name = f_file.url.rsplit("/", 1)
                v_name = name.rsplit(".", 1)[0] + "." + v["extension"]
                v_url = "/".join([base_url, v["name"], v_name])
                setattr(f_file, v["name"] + "_url", v_url)
            else:
                setattr(f_file, v["name"] + "_url", v["default_url"])

    def contribute_to_class(self, cls, name):
        """
        Call methods for generating all operations on specified signals
        """
        super(SvgManipulationField, self).contribute_to_class(cls, name)
        # signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self.__add_attributes, sender=cls)
        # signals.pre_delete.connect(self._remove_all_data_signal, sender=cls)