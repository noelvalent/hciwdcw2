'''
This is a model for listing backup files.

It cannot be created and deleted by any user.
'''

from django.db import models
from django.utils import timezone


class Backup(models.Model):
    created_by = models.DateTimeField(default=timezone.now, help_text='creation date')
    backup_file = models.FileField(upload_to='backup')

    def __str__(self):
        return str(self.backup_file.name)
