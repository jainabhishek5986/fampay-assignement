from django.db import models


class Video(models.Model):
    title = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=255)
    video_url = models.URLField(max_length=255)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class APIKey(models.Model):
    key = models.CharField(max_length=255)
    is_limit_over = models.BooleanField(default=False)

    class Meta:
        verbose_name = "APIKey"
        verbose_name_plural = "APIKeys"

    def __str__(self):
        return self.key
