from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly  # , IsAuthenticated
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from blog.models import Post,  Category


# @api_view(['GET', 'PUT', 'DELETE'])
# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id, status=True)
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response({'detail': 'item removed successfully'},
#                         status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# @dec_permission_classes([IsAuthenticatedOrReadOnly])
# def post_list(request):
#     if request.method == 'GET':
#         posts = Post.objects.filter(status=True)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(request.data)


# class PostList(APIView):
#     """
#     API view for post list operations (GET/POST).
#     Handles retrieving all published posts
#     and creating new posts with validation.
#     """

#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer

#     def get(self, request):
#         """
#         Retrieves all published posts (status=True)
#         and returns serialized data.
#         Returns JSON response containing post data.
#         """

#         posts = Post.objects.filter(status=True)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         """
#         Creates a new blog post using provided data from the request.
#         Validates and saves the post data,
#         returning the created post details in the response.
#         """

#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(request.data)


class PostDetail(RetrieveUpdateDestroyAPIView):
    """
    API view for post detail operations (GET/PUT/DELETE).
    Handles retrieving, updating, and deleting a single post.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    lookup_field = 'id'


class PostList(ListCreateAPIView):
    """
    Generic API view for post list operations (GET/POST).
    Inherits from ListCreateAPIView to provide built-in
    list and create operations with automatic serialization.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


# Example for viewsets in CBV
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    
    @action(methods=['get'], detail=False)
    def get_ok(self, request):
        return Response({'detail': 'ok'})


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
