from django.test import TestCase
from blog.models import Post, Category
from accounts.models import User, Profile
from django.utils import timezone


class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="123456789.Ab"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test_name',
            last_name='test_l_name',
            bio='test_bio'
        )
        
    def test_create_post_with_valid_data(self):
        
        post = Post.objects.create(
            author=self.profile,
            title='test',
            content='test content',
            status=1,
            category=None,
            published_date=timezone.now()
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())