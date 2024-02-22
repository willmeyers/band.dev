from django.db import models
from django.utils import timezone

from band_dev.utils import make_readable_id


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def readable_id(self):
        return make_readable_id(id=self.id)
