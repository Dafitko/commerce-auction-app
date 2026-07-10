import random

from django.core.management.base import BaseCommand

from auctions.models import Auction_listing, Bid, Category, Comment, User

USERS = ["test", "bob", "carol", "dave"]

CATEGORIES = ["Electronics", "Books", "Home", "Toys", "Fashion"]

LISTINGS = [
    ("Vintage Camera", "A classic film camera in great condition.", 40, "Electronics",
     "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f"),
    ("Mountain Bike", "Lightly used mountain bike, 21-speed.", 150, "Home",
     "https://images.unsplash.com/photo-1485965120184-e220f721d03e"),
    ("Sci-Fi Novel Collection", "Set of 5 classic sci-fi novels.", 15, "Books",
     "https://images.unsplash.com/photo-1512820790803-83ca734da794"),
    ("Wireless Headphones", "Noise-cancelling over-ear headphones.", 60, "Electronics",
     "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"),
    ("Board Game Bundle", "Three popular strategy board games.", 25, "Toys",
     "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09"),
    ("Leather Jacket", "Genuine leather jacket, size M.", 80, "Fashion",
     "https://images.unsplash.com/photo-1551028719-00167b16eac5"),
]


class Command(BaseCommand):
    help = "Populate the database with demo data"

    def handle(self, *args, **options):
        users = []
        for username in USERS:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": f"{username}@example.com"}
            )
            if created:
                user.set_password("test")
                user.save()
            users.append(user)

        categories = {}
        for name in CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category

        for title, description, starting_bid, category_name, image_url in LISTINGS:
            listing, created = Auction_listing.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "starting_bid": starting_bid,
                    "category": categories[category_name],
                    "image_url": image_url,
                    "user": random.choice(users),
                },
            )
            if created:
                for _ in range(random.randint(0, 3)):
                    bidder = random.choice(users)
                    current = listing.current_price()
                    Bid.objects.create(
                        listing=listing, user=bidder, value=current + random.randint(5, 20)
                    )
                for _ in range(random.randint(0, 2)):
                    commenter = random.choice(users)
                    Comment.objects.create(
                        listing=listing, user=commenter, content="Great item, still interested!"
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(users)} users, {len(categories)} categories, {len(LISTINGS)} listings. "
            "Demo login: alice / password123"
        ))
