import random

from django.core.management.base import BaseCommand
import bcrypt
from faker import Faker
from faker.providers import internet, person, date_time, lorem, barcode

from Fridgify_Backend import models


class Command(BaseCommand):
    help = "Fills the database with randomized data for testing"
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fridges', type=int, help="Number of fridges")
        parser.add_argument('-u', '--users', type=int, help="Number of users")
        parser.add_argument('-i', '--items', type=int, help="Number of items")
        parser.add_argument('-fc', '--fridgecontent', type=int, help="Max amount of items in fridge")
        parser.add_argument('-upf', '--userpfridge', type=int, help="Amount of users per fridge")

    def handle(self, *args, **options):
        p_fridges = 3 if options["fridges"] is None else options["fridges"]
        p_users = 5 if options["users"] is None else options["users"]
        p_items = 5 if options["items"] is None else options["items"]
        p_upf = 2 if options["userpfridge"] is None else options["userpfridge"]
        p_fc = 3 if options["fridgecontent"] is None else options["fridgecontent"]
        
        self.stdout.write(f"Fill database with: \n" +
            f"Fridges: {p_fridges}, Users: {p_users+1}, User per Fridge: {p_upf}, Items: {p_items}, Max. Items per fridge: {p_fc}")

        self.fake.add_provider(internet)
        self.fake.add_provider(person)
        self.fake.add_provider(date_time)
        self.fake.add_provider(lorem)
        self.fake.add_provider(barcode)

        self.create_users(p_users)
        self.create_fridge(p_fridges)
        self.connect_uf(p_users, p_upf)
        self.create_store()
        self.create_item(p_items)
        self.fill_fridges(p_fc)

        self.stdout.write(f"Database was filled successfully...")

    def create_users(self, count):
        for i in range(count):
            user = models.Users.objects.create(
                username=self.fake.user_name(),
                name=self.fake.last_name(),
                surname=self.fake.first_name(),
                email=self.fake.email(),
                password=bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()),
                birth_date=self.fake.date_of_birth().strftime("%Y-%m-%d")
            )
        models.Users.objects.create(
            username="fridgify_test",
            name="Fridgify",
            surname="Test",
            email="fridgify@fridgify.com",
            password=bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()),
            birth_date=self.fake.date_of_birth().strftime("%Y-%m-%d")
        )
        self.users = models.Users.objects.all()

    def create_fridge(self, count):
        for i in range(count):
            fridge = models.Fridges(
                name=self.fake.word(),
                description=self.fake.text()
            )
            fridge.save()
        self.fridges = models.Fridges.objects.all()

    def connect_uf(self, user_count, upf=1):
        ufs = []
        for fridge in self.fridges:
            exclude = []
            ufs.append(models.UserFridge(
                user=models.Users.objects.get(username="fridgify_test"),
                fridge=fridge,
                role=0
            ))
            for i in range(upf):
                rand = random.randint(0, user_count-1)
                while rand in exclude:
                    rand = random.randint(0, user_count-1)
                
                ufs.append(models.UserFridge(
                    user=self.users[rand],
                    fridge=fridge,
                    role=random.randint(1, 2)
                ))
                exclude.append(rand)
        models.UserFridge.objects.bulk_create(ufs)

    def create_store(self):
        models.Stores.objects.bulk_create([
            models.Stores(name="Rewe"),
            models.Stores(name="Aldi Süd"),
            models.Stores(name="Penny"),
            models.Stores(name="Lidl"),
            models.Stores(name="Nahkauf"),
        ])
        self.stores = models.Stores.objects.all()

    def create_item(self, count):
        for i in range(count):
            models.Items.objects.create(
                barcode=self.fake.ean(),
                name=self.fake.word(),
                description=self.fake.sentence(),
                store=self.stores[random.randint(0, (count-1))]
            )
        self.items = models.Items.objects.all()

    def fill_fridges(self, max_items):
        fc = []
        units = ["kg", "g", "l", "ml"]
        for fridge in self.fridges:
            for i in range(random.randint(1, max_items)):
                fc.append(
                    models.FridgeContent(
                        fridge=fridge,
                        item=self.items[random.randint(0, (len(self.items)-1))],
                        amount=random.randint(0, 1000),
                        unit=units[random.randint(0, 3)],
                        expiration_date=self.fake.future_date().strftime("%Y-%m-%d"),
                    )
                )
        models.FridgeContent.objects.bulk_create(fc)
        