from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'email': serializer.validated_data['email'],
            'message': 'User registered successfully'
        }
        return Response(
            data,
            status=status.HTTP_201_CREATED
        )
