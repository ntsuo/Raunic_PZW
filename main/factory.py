import factory
from factory.django import DjangoModelFactory
from main.models import *


class UmjetnikFactory(DjangoModelFactory):
    class Meta:
        model = Umjetnik

    ime = factory.Faker("first_name")
    prezime = factory.Faker("last_name")
    biografija = factory.Faker("paragraph")
    #slike_umjetnika = factory.django.ImageField(filename='example.jpg')

   
class DjeloFactory(DjangoModelFactory):
    class Meta:
        model = Djelo

    naslov = factory.Faker('sentence', nb_words=3)
    umjetnik = factory.SubFactory('main.factory.UmjetnikFactory')
    opis = factory.Faker('paragraph')
    slika = factory.django.ImageField(filename='example.jpg')
    datum_stvaranja = factory.Faker('date_time')
    medij = factory.Faker('word')

  
class KulturniDogadajFactory(DjangoModelFactory):
    class Meta:
        model = KulturniDogadaj

    ime = factory.Faker('sentence', nb_words=6)
    opis = factory.Faker('paragraph')
    datum = factory.Faker('date_time')
    vrijeme = factory.Faker('time')
    lokacija = factory.Faker('address')
    organizator = factory.Faker("first_name")