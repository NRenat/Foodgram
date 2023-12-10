from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .validators import hex_color_validator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Tag')
    color = models.CharField(max_length=7, unique=True,
                             validators=(hex_color_validator,),
                             verbose_name='Color HEX')
    slug = models.SlugField(max_length=64, unique=True,
                            verbose_name='Slug for Tag')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=64, verbose_name='Ingredient')
    measurement_unit = models.CharField(max_length=10,
                                        verbose_name='Measurement Unit')

    class Meta:
        unique_together = ('name', 'measurement_unit')
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author recipe'
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Recipe name'
    )
    image = models.ImageField(
        verbose_name='Picture',
    )
    text = models.TextField(
        verbose_name='Recipe description'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=(MinValueValidator(1, message='Value must be at least 1'),))
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Recipe Ingredients',
                                         through='RecipeIngredient')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ingredient')
    amount = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Amount of ingredients',
        validators=(MinValueValidator(1, message='Value must be at least 1'),)
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE,
                             related_name='shopping_carts',
                             verbose_name='User')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_carts',
                               verbose_name='Recipe')

    class Meta:
        verbose_name = 'Recipe in the shopping list'
        verbose_name_plural = 'Recipes in the shopping list'
        constraints = (
            UniqueConstraint(
                fields=(
                    'recipe',
                    'user',
                ),
                name='unique_recipe_cart',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.name} -> {self.recipe.name}'


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites', verbose_name='Recipe')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites', verbose_name='User')

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = (
            UniqueConstraint(fields=('recipe', 'user'),
                             name='unique_favorite'),
        )

    def __str__(self) -> str:
        return f'{self.user.name} -> {self.recipe.name}'
