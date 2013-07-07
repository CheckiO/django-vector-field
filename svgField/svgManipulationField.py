
from django.db.models import signals
from django.db import models
from django.db.models.fields.files import FieldFile
import os

class VersionFile():
    def __init__(self, field_file, version):
        if not field_file:
            self.path = None
            self.url = version.default_url
        else:
            base_url, file_name = field_file.url.rsplit("/", 1)
            base_name = file_name.rsplit(".", 1)[0]
            base_path = os.path.split(field_file.path)[0]
            ext = version.converter.extension
            ver_file_name = ".".join([base_name, ext]) if ext else ""
            self.path = os.path.join(base_path, version.name, ver_file_name)
            if os.path.exists(self.path):
                self.url = "/".join([base_url, version.name, ver_file_name])
            else:
                self.url = version.default_url

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

        field_file = getattr(instance, self.name)

        for v in self.versions:
            if field_file:
                ver_file = VersionFile(field_file, v)
            else:
                ver_file = VersionFile(None, v)
            setattr(field_file, v.name, ver_file)

    def contribute_to_class(self, cls, name):
        """
        Call methods for generating all operations on specified signals
        """
        super(SvgManipulationField, self).contribute_to_class(cls, name)
        # signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self.__add_attributes, sender=cls)
        # signals.pre_delete.connect(self._remove_all_data_signal, sender=cls)