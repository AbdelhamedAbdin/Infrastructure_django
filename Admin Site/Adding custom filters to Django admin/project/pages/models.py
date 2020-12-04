from django.db import models


class Website(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url


class Page(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    url = models.URLField(max_length=2083)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.url
