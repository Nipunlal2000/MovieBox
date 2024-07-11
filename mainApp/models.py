from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return '{}'.format(self.username)


class LoginTable(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.username)


class Genres(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/')
    description = models.CharField(max_length=5000)
    release_year = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    genres = models.ForeignKey(Genres, on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(LoginTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'
