from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework import status


# не полная информация
@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        products = models.Product.objects.all()
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # print(request.data)
        # title = request.data.get('title')
        # description = request.data.get('description')
        # price = request.data.get('price')
        # category_id = request.data.get('category_id')
        # # Product.objects.create(title=title, description=description, price=price,
        # # category_id=category_id)
        # product = Product.objects.create(title=title, description=description, price=price,
        #                                  category_id=category_id)
        # # return Response(data={'message': 'Data Received'})
        product = models.Product.objects.create(**request.data)
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


@api_view(['GET'])
def test(request):
    context = {
        'integer': 100,
        'string': 'hello world',
        'boolean': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=context)
