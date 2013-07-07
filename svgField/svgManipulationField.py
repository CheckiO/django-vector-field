
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

    def get_db_prep_save(self, value, connection):
        if value:
            for version in self.versions:
                version.write_version_file(value.path)
        return self.get_prep_value(value)

    def __add_attributes(self, instance, **kwargs):

        f_file = getattr(instance, self.name)

        for v in self.versions:
            if f_file:
                base_url, name = f_file.url.rsplit("/", 1)
                v_name = name.rsplit(".", 1)[0] + "." + v.converter.extension
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