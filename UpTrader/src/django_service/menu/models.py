from django.db import models
from django.urls import reverse_lazy


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        if self.named_url:
            return reverse_lazy(self.named_url)

        if self.parent:
            return self.parent.get_absolute_url() + "/" + self.url

        return self.url
