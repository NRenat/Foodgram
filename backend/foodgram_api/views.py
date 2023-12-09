from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reportlab.pdfgen import canvas
from io import BytesIO

from foodgram.models import Recipe, Ingredient, Tag, Favorite, ShoppingCart, \
    RecipeIngredient
from foodgram_backend.settings import PDF_NAME
from .serializers import RecipeSerializer, IngredientSerializer, TagSerializer
from .serializers import RecipeWriteSerializer, FavoriteSerializer, \
    ShoppingCartSerializer
from .permissions import OwnerAdminReadOnly
from .filters import RecipeFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerAdminReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(
        methods=('post',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite, user=user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('post',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = get_object_or_404(
            ShoppingCart, user=user, recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_carts__user=request.user
        ).order_by(
            'ingredient__name'
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100, 800, 'Shopping Cart:')
        y_position = 780
        for ingredient in ingredients:
            line = (f'{ingredient["ingredient__name"]} - '
                    f'{ingredient["ingredient_total"]} '
                    f'{ingredient["ingredient__measurement_unit"]}')
            pdf.drawString(100, y_position, line)
            y_position -= 20

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response[
            'Content-Disposition'] = f'attachment; filename="{PDF_NAME}"'
        return response
