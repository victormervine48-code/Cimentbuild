from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.store.models import Category, Product, DeliveryZone

class Command(BaseCommand):
    help = "Crée le catalogue de démonstration CimentBuild"

    def handle(self, *args, **kwargs):
        data = {
            "Ciment": [("Ciment Portland 50 kg", 4500, "sac", 100)],
            "Gravier": [("Gravier concassé", 18000, "m3", 50)],
            "Sable": [("Sable de construction", 12000, "m3", 50)],
            "Fer": [("Fer à béton 8 mm", 3500, "barre", 200)],
            "Briques": [("Parpaing 15", 350, "piece", 1000)],
            "Bois": [("Planche de coffrage", 5000, "piece", 200)],
            "Plomberie": [("Tube PVC 32 mm", 2500, "piece", 100)],
            "Électricité": [("Câble électrique 2,5 mm²", 3500, "piece", 100)],
        }
        for cname, products in data.items():
            category, _ = Category.objects.get_or_create(name=cname, defaults={"slug": slugify(cname)})
            for name, price, unit, stock in products:
                Product.objects.get_or_create(name=name, category=category, defaults={"price":price,"unit":unit,"stock":stock,"description":f"{name} — produit de démonstration."})
        DeliveryZone.objects.get_or_create(name="Lomé", defaults={"fee":0})
        DeliveryZone.objects.get_or_create(name="Périphérie de Lomé", defaults={"fee":2000})
        self.stdout.write(self.style.SUCCESS("Catalogue et zones créés."))
