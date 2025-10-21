from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import User, Profile


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="test@test.test", password="Testpass1234@", is_verified=True
    )
    return user


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestPostsAPI:

    def test_get_posts_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "test content",
            "status": True,
            "published_date": timezone.now(),
        }
        user = common_user
        # api_client.force_login(user=user)
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201
