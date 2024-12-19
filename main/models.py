from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Umjetnik(models.Model):
    ime = models.CharField(max_length=100)
    prezime = models.CharField(max_length=100)
    biografija = models.TextField(blank=True)
    slike_umjetnika = models.ManyToManyField('Djelo', related_name='umjetnik_slika', blank=True)

    def __str__(self):
        return self.ime

class Djelo(models.Model):
    naslov = models.CharField(max_length=255)
    umjetnik = models.ForeignKey(Umjetnik, on_delete=models.CASCADE)
    opis = models.TextField(blank=True)
    slika = models.ImageField(upload_to='djela/')
    datum_stvaranja = models.DateTimeField(auto_now_add=True)
    medij = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.naslov

class KulturniDogadaj(models.Model):
    ime = models.CharField(max_length=255)
    opis = models.TextField()
    datum = models.DateField()
    vrijeme = models.TimeField()
    lokacija = models.CharField(max_length=255)
    organizator =models.CharField(max_length=255)
    umjetnicka_djela = models.ManyToManyField(Djelo, blank=True)

    def __str__(self):
        return self.ime