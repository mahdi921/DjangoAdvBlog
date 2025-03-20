from rest_framework import serializers
from blog.models import Post, Category


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'category', 'status',
            'created_date', 'updated_date', 'published_date'
        )


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
