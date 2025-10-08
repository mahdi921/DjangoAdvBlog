from django.test import TestCase
from blog.forms import PostForm
from blog.models import Category
from django.utils import timezone


class TestPostForm(TestCase):
    def test_post_form_with_valid_data(self):
        category_obj = Category.objects.create(name='test category')

        form = PostForm(data={
            'title': 'test',
            'content': 'hello',
            'category': category_obj,
            'status': 1,
            'published_date': timezone.now()
        })
        self.assertTrue(form.is_valid(), 'form is not valid')
