from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from product.models import Review
from product.serializers import ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()  # Добавляем атрибут queryset
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['text', 'product']


class ReviewUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()  # Добавляем атрибут queryset
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class RegisterAPIView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # username = request.data.get('username')
        # password = request.data.get('password')
        User.objects.create_user(**serializer.validated_data)
        return Response(data={"message": "User Created"}, status=status.HTTP_201_CREATED)
