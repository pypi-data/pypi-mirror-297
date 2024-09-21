from django.db import models

# Create your models here.
from django.db import models


class PackageTest(models.Model):
    """Model for KYC TYPE Master"""
    type_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.type_name)

    class Meta:
        db_table = 'package_test'
