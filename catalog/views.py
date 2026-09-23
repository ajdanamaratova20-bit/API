from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category, Review
from .filters import ProductFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly, IsReviewAuthorOrReadOnly
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Avg


@extend_schema_view(
    list=extend_schema(
        summary='Получить список категорий',
        tags=['Категории'],
    ),
    retrieve=extend_schema(
        summary='Получить одну категорию',
        tags=['Категории'],
    ),
    create=extend_schema(
        summary='Создать категорию',
        tags=['Категории'],
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer

    def get_queryset(self):
        return Category.objects.prefetch_related("products")



@extend_schema_view(
    list=extend_schema(
        summary='Получить список товаров',
        tags=['Товары'],
    ),
    retrieve=extend_schema(
        summary='Получить один товар',
        tags=['Товары'],
    ),
    create=extend_schema(
        summary='Создать товар',
        tags=['Товары'],
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at","in_stock"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.select_related(
            "category"
        ).prefetch_related(
            "reviews"
        )

    def get_queryset(self):
        return (
            Product.objects
            .select_related('category')
            .annotate(average_rating=Avg('reviews__rating'))
            .order_by('-created_at')
        )

    def get_queryset(self):
        return (
            Product.objects
            .select_related('category')
            .annotate(average_rating=Avg('reviews__rating'))
            .order_by('-created_at')
        )


@extend_schema_view(
    list=extend_schema(
        summary='Получить список отзывов',
        tags=['Отзывы'],
    ),
    retrieve=extend_schema(
        summary='Получить один отзыв',
        tags=['Отзывы'],
    ),
    create=extend_schema(
        summary='Создать отзыв',
        tags=['Отзывы'],
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsReviewAuthorOrReadOnly
    ]
    filterset_fields = ["product"]

    def get_queryset(self):
        return Review.objects.select_related("user", "product")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

