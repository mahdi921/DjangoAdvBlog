from django.db import models
from django.urls import reverse
# from django.contrib.auth import get_user_model

# get user model object
# User = get_user_model()


class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    # login_required = models.BooleanField(default=False)
    # staff_only = models.BooleanField(default=False)
    # hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def get_snippet(self):
        return self.content[:5]

    def __str__(self):
        return self.title

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
