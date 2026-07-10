import random

from django.core.management.base import BaseCommand

from auctions.models import Auction_listing, Bid, Category, Comment, User

USERS = ["harry", "ron", "hermione", "malfoy"]

CATEGORIES = ["Wands & Spellwork", "Potions & Ingredients", "Quidditch Gear", "Creatures", "Cursed Objects"]

LISTINGS = [
    ("Elder Wand (slightly used)", "Previous owner deceased. Undefeated in duels, allegedly. "
     "Selling due to moving flats, no longer need to conquer death.", 500, "Wands & Spellwork",
     "https://images.unsplash.com/photo-1519791883288-dc8bd696e667"),
    ("Nimbus 2000, one careful owner", "Barely flown, except into a Whomping Willow once. "
     "Comes with minor scratches and a strong desire to seek revenge on said tree.", 120, "Quidditch Gear",
     "https://images.unsplash.com/photo-1519741497674-611481863552"),
    ("Half-used Polyjuice Potion", "Enough for one (1) transformation. Buyer assumes all risk of "
     "becoming someone's least favorite professor. Cat hair not included, allegedly.", 35, "Potions & Ingredients",
     "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108"),
    ("Slightly Cursed Locket", "Whispers occasionally. Does not require a Horcrux-removal "
     "specialist, probably. Sold as-is, no refunds, no exceptions, no arguing with it.", 66, "Cursed Objects",
     "https://images.unsplash.com/photo-1518709268805-4e9042af2176"),
    ("Baby Norwegian Ridgeback", "Free to a good home outside of Scotland. Hatched accidentally "
     "during a Care of Magical Creatures assignment. Breathes fire when hungry, so often.", 200, "Creatures",
     "https://images.unsplash.com/photo-1560743641-3914f2c45636"),
    ("Invisibility Cloak, family heirloom", "Passed down for generations, works perfectly, "
     "still haven't found where I left my other socks though. Genuine, not a knockoff.", 750, "Cursed Objects",
     "https://images.unsplash.com/photo-1509248961158-e54f6934749c"),
]

COMMENTS = [
    "Does this come with a certificate of authenticity from Ollivanders?",
    "Asking for a friend who is definitely not planning anything illegal at Hogwarts.",
    "Is the cursed part negotiable?",
    "Bought something similar once. Would not recommend. 0/10 tried to kill me.",
    "My owl approves of this listing.",
    "Does it work on Muggles too, or just wizards?",
]


class Command(BaseCommand):
    help = "Populate the database with Harry Potter themed demo data"

    def handle(self, *args, **options):
        users = []
        for username in USERS:
            user, created = User.objects.get_or_create(
                username=username, defaults={"email": f"{username}@hogwarts.edu"}
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
                        listing=listing, user=commenter, content=random.choice(COMMENTS)
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(users)} wizards, {len(categories)} categories, {len(LISTINGS)} listings. "
            "Demo login: harry / test"
        ))
