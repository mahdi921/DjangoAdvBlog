from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
import random
from django.utils import timezone

category_list = [
    "Technology",
    "Health",
    "Travel",
    "Food",
    "Lifestyle",
    "Education",
    "Finance",
    "IT",
]


class Command(BaseCommand):
    help = "Inserts fake data into blog app for testing purposes"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(), password="Test@987654321"
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.bio = self.fake.text(max_nb_chars=100)
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name=name)

        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.fake.sentence(nb_words=6),
                content=self.fake.text(max_nb_chars=2000),
                category=Category.objects.get(name=random.choice(category_list)),
                status=random.choice([True, False]),
                published_date=timezone.now(),
            )
