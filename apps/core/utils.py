import uuid
import os
from datetime import date

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, instance, filename):
        today = date.today()
        ext = os.path.splitext(filename)[1].lower()
        return os.path.join(
            self.path, str(today.year), str(today.month), f"{uuid.uuid4()}{ext}"
        )
