from django.db import models

# Create your models here.

class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    author = models.Foreignkey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=SET_NULL, null=True)
    status = models.BooleanField(default=False)
    # login_required = models.BooleanField(default=False)
    # staff_only = models.BooleanField(default=False)
    # hidden = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name