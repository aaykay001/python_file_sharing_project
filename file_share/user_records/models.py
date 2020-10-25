from django.db import models
from django.contrib.auth.models import User


class FileInfo(models.Model):
    admin_id = models.IntegerField()
    admin_user_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    shared_with = models.ManyToManyField(User)
    file_url = models.URLField(max_length=200)
    file_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True, blank=True)

    def __str__(self):
        return "Admin {} uploaded this {} at {}".format(self.admin_id,
                                                        self.file_name,
                                                        self.created_at)
