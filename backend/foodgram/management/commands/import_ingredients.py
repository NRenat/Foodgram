import csv
from django.core.management.base import BaseCommand

from foodgram.models import Ingredient


class Command(BaseCommand):
    help = 'import ingredients from data/ingredients.csv'

    def handle(self, *args, **options):
        try:
            with open('./data/ingredients.csv', 'r',
                      encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    name, measurement_unit = row[0], row[1]
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f'Add ingredient: {ingredient}'))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'Ingredient already exists: {ingredient}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}'))
