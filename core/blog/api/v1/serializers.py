from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(
        source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    # category = CategorySerializer()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'image', 'content', 'category', 'status',
            'created_date', 'updated_date', 'published_date',
            'snippet', 'relative_url', 'absolute_url',
        )
        read_only_fields = ('author',)

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        represntation = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            represntation.pop('snippet', None)
            represntation.pop('relative_url', None)
            represntation.pop('absolute_url', None)
        else:
            represntation.pop('content', None)
        represntation['category'] = CategorySerializer(
            instance.category,
            context={'request': request}
        ).data
        return represntation

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(
            user__id=self.context.get('request').user.id)
        return super().create(validated_data)
