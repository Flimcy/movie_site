from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    GENRES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci-fi', 'Sci-Fi'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    thumbnail_file = models.ImageField(upload_to='movie_thumbnails/', null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    banner_url = models.URLField(null=True, blank=True)
    watch_link = models.URLField()
    trailer_link = models.URLField()
    release_date = models.DateField()

    def __str__(self):
        return self.title