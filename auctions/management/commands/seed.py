from decimal import Decimal

from django.core.management.base import BaseCommand

from auctions.models import User, Category, Auction_listing


LISTINGS = [
    ("Nimbus 2000 Broomstick", "A racing broom once used in professional Quidditch.", 80, "Toys",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Broom_icon.svg/512px-Broom_icon.svg.png"),
    ("Vintage Vinyl Record Player", "Fully working turntable from the 70s, great sound.", 45, "Electronics",
     "https://images.unsplash.com/photo-1461360370896-922624d12aa1"),
    ("Leather Jacket", "Genuine leather, size M, barely worn.", 30, "Fashion",
     "https://images.unsplash.com/photo-1551028719-00167b16eac5"),
    ("Mechanical Keyboard", "RGB backlit, brown switches.", 60, "Electronics",
     "https://images.unsplash.com/photo-1587829741301-dc798b83add3"),
    ("Antique Wooden Desk", "Solid oak desk with three drawers.", 120, "Home",
     "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd"),
    ("Mountain Bike", "21-speed, lightly used, great condition.", 150, "Toys",
     "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91"),
    ("Board Game Collection", "Bundle of 5 classic board games.", 25, "Toys",
     "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09"),
    ("Espresso Machine", "Barely used, makes great coffee.", 90, "Home",
     "https://images.unsplash.com/photo-1585441695532-19f7ae0f9264"),
    ("Denim Jacket", "Classic blue denim, size L.", 20, "Fashion",
     "https://images.unsplash.com/photo-1544022613-e87ca75a784a"),
    ("Wireless Headphones", "Noise-cancelling, 30h battery life.", 55, "Electronics",
     "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"),
    ("Ceramic Vase Set", "Set of 3 handmade ceramic vases.", 15, "Home",
     "https://images.unsplash.com/photo-1578500494198-246f612d3b3d"),
    ("Retro Sunglasses", "80s style, UV protection.", 10, "Fashion",
     "https://images.unsplash.com/photo-1511499767150-a48a237f0083"),
]

CATEGORY_NAMES = ["Electronics", "Fashion", "Toys", "Home", "Books"]

TEST_USERNAMES = ["test1", "test2", "test3", "test4", "test5"]
TEST_PASSWORD = "password123"


class Command(BaseCommand):
    help = "Seed the database with test users, categories, and listings."

    def handle(self, *args, **options):
        users = []
        for username in TEST_USERNAMES:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@example.com"}
            )
            if created:
                user.set_password(TEST_PASSWORD)
                user.save()
            users.append(user)

        categories = {}
        for name in CATEGORY_NAMES:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category

        created_count = 0
        for i, (title, description, starting_bid, category_name, image_url) in enumerate(LISTINGS):
            if Auction_listing.objects.filter(title=title).exists():
                continue

            Auction_listing.objects.create(
                user=users[i % len(users)],
                title=title,
                description=description,
                starting_bid=Decimal(starting_bid),
                category=categories[category_name],
                image_url=image_url,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(users)} users (password: {TEST_PASSWORD}), "
            f"{len(categories)} categories, {created_count} new listings."
        ))
