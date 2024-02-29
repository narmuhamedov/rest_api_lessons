from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        # fields = '__all__'
        fields = 'id title price category reviews count_reviews all_reviews rating'.split()

    def get_category(self, product):
        try:
            return f'{product.category.id} - {product.category.name}'
        except:
            return "No Category"

    def get_reviews(self, product):
        # serializer = ReviewSerializer(product.reviews.all(), many=True)
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False,
                                                                   product=product), many=True)
        return serializer.data


# class ObjectCreateSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     is_active = serializers.BooleanField()
#

class ReviewCreateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=50)


class ProductCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=10)
    description = serializers.CharField()
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
    reviews = serializers.ListField(child=ReviewCreateSerializer())

    # list_ = serializers.ListField(child=serializers.CharField())
    # #object_ = {"name": "Sofa", "is_active": True}
    # object_ = ObjectCreateSerializer()

    def validate_category_id(self, category_id):
        if models.Category.objects.filter(id=category_id).count() == 0:
            raise ValidationError(f"Category with id {category_id} does not exist")

        return category_id

    # def validate(self, attrs):
    #     id = attrs['category_id']
    #     try:
    #         models.Category.objects.get(id=id)
    #     except models.Category.DoesNotExist:
    #         raise ValidationError(f"Category with id {id} does not exist")
    #     return attrs
