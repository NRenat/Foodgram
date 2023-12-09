from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import FollowApiView, FollowListAPIView
from .views import RecipeViewSet, IngredientViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = (
    path(
        'users/<int:id>/subscribe/',
        FollowApiView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        FollowListAPIView.as_view(),
        name='subscription'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
)
