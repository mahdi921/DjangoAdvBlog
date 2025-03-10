from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from blog.models import Post
from django.shortcuts import get_object_or_404


@api_view()
def post_list(request):
    return Response({"details": "Hello, world!"})


@api_view()
def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=True)
    serializer = PostSerializer(post)
    return Response(serializer.data)
