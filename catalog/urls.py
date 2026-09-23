from .views import CategoryViewSet, ProductViewSet, ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("reviews", ReviewViewSet, basename="review")


urlpatterns = router.urls