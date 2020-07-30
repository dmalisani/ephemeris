from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class RegisteredDate(models.Model):
    registered_on = models.DateTimeField(auto_now_add=True)
    registered_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    date = models.DateField(verbose_name=_("date"))
    title = models.CharField(max_length=50, verbose_name=_("title"))
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
