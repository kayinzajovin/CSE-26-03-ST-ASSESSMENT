from django.db import models


# Store each uploaded video together with its metadata.
class Video(models.Model):
    # These are the quality labels users can choose from.
    QUALITY_CHOICES = [
        ('360p', '360p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4k', '4K'),
    ]

    # The title of the video.
    title = models.CharField(max_length=200)
    # Optional description text.
    description = models.TextField(blank=True)
    # The selected quality from the dropdown.
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    # The user-provided publish date.
    publish_date = models.DateField()
    # The actual uploaded video file.
    video_file = models.FileField(upload_to='videos/')
    # Optional thumbnail image for the video.
    thumbnail_file = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    # Timestamp when the record was created.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
