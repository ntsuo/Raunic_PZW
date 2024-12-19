import random
from django.db import transaction
from django.core.management.base import BaseCommand
from main.models import Umjetnik, Djelo, KulturniDogadaj
from main.factory import (
    UmjetnikFactory,
    DjeloFactory,
    KulturniDogadajFactory,
)

NUM_UMJETNIKA = 10
NUM_DJELA = 100
NUM_DOGADJAJA = 50

class Command(BaseCommand):
    help = "Generira testne podatke za umjetnike, djela i kulturne događaje"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Brisanje starih podataka...")

        models = [Umjetnik, Djelo, KulturniDogadaj]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Kreiranje novih podataka...")
        umjetnici = [UmjetnikFactory() for _ in range(NUM_UMJETNIKA)]

        for _ in range(NUM_DJELA):
            umjetnik = random.choice(umjetnici) 
            DjeloFactory(umjetnik=umjetnik) 

        for _ in range(NUM_DOGADJAJA):
            kulturni_dogadaj = KulturniDogadajFactory()

            # povezivanje događaja s djelo
            djela = random.sample(list(Djelo.objects.all()), k=random.randint(1, 5))
            kulturni_dogadaj.umjetnicka_djela.set(djela)
