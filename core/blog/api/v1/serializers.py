from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    created_date = serializers.DateTimeField()
    updated_date = serializers.DateTimeField()
    published_date = serializers.DateTimeField()