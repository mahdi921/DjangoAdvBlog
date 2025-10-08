from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from blog.models import Post, Category
from django.utils import timezone


class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.post = Post.objects.create(
            author=self.profile,
            title='test',
            content='test content',
            status=1,
            category=None,
            published_date=timezone.now()
        )

    def test_blog_index_url_response_200(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_post_detail_loggged_in_response(self):
        self.client.force_login(self.user)
        url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_post_detail_anonymous_response(self):
        url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
