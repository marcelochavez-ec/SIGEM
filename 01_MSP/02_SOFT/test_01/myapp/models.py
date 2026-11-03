from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)