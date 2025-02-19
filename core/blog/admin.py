from django.contrib import admin
from blog.models import Post, Category

# Register post model here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status',
                    'created_date', 'published_date'
                    ]
    list_filter = ['status', 'published_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_date'


# Register Category model here.
admin.site.register(Category)
