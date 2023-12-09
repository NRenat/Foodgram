from django.contrib import admin
from foodgram.models import Tag, Ingredient, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author'
    )
    search_fields = (
        'author',
        'name'
    )
    list_filter = (
        'name',
        'author'
    )
