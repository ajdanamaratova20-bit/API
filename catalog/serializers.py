from rest_framework import serializers
from .models import Product, Category,Review
from django.core.validators import RegexValidator
from django.db.models import Avg
from rest_framework import serializers
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9-]+$',
                message='Slug может содержать только латинские буквы, цифры и дефисы.'
            )
        ]
    )

    class Meta:
        model = Category
        fields =  ["id","name","slug","created_at"]




class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    average_rating = serializers.SerializerMethodField()
    
    def validate_in_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Остаток не может быть отрицательным."
            )
        return value

    def validate(self, attrs):
        if len(attrs["name"]) < 2:
            raise serializers.ValidationError(
                "Название товара должно содержать минимум 2 символа."
            )
        return attrs

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше нуля."
            )
        return value



    def get_average_rating(self, obj):
        average = getattr(obj, 'average_rating', None)

        if average is None:
            average = obj.reviews.aggregate(
                average=Avg('rating')
            )['average']

        return float(average) if average is not None else None


    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "price",
            "in_stock",
            "created_at",
            "updated_at",
            "owner",
            'average_rating',
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "category_name",
        ]

    owner = serializers.ReadOnlyField(source="owner.username")

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "comment", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5."
            )
        return value

class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ProductSerializer.Meta.fields + ["reviews"]


class CategoryDetailSerializer(CategorySerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = CategorySerializer.Meta.fields + ["products"]

average_rating = serializers.SerializerMethodField()
def get_average_rating(self, obj):
    average = getattr(obj, 'average_rating', None)

    if average is None:
        average = obj.reviews.aggregate(
            average=Avg('rating')
        )['average']

    return float(average) if average is not None else None