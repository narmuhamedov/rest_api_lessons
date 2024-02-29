from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# не полная информация
@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        products = models.Product.objects.all()
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = serializers.ProductCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

        print(request.data)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = models.Product.objects.create(title=title, description=description, price=price,
                                                category_id=category_id)
        for i in request.data.get('reviews', []):
            models.Review.objects.create(stars=i['stars'], text=i['text'], product=product)

        # return Response(data={'message': 'Data Received'})
        # product = models.Product.objects.create(**request.data)
        return Response(data=serializers.ProductSerializer(product).data,
                        status=status.HTTP_201_CREATED)


# Детальная информация изменение и удаление
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, id):
    try:
        product = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Product not found'})

    if request.method == 'GET':
        data = serializers.ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Product has been deleted'})
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(data=serializers.ProductSerializer(product).data)


from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def authorization(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()
            #     try:
            #         token = Token.objects.get(user=user)
            #     except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)

    return Response(data={'error': "user not found"}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth.models import User


@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create_user(username=username, password=password)
        return Response(data={"message": "User Created"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    reviews = models.Review.objects.filter(author=request.user)
    serializer = serializers.ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def test(request):
    print(request.user)
    context = {
        'integer': 100,
        'string': 'hello world',
        'boolean': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=context)
