from io import BytesIO
from django.http import HttpResponse
from django.db.models import Sum
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.models import RecipeIngredient
from foodgram_backend.settings import PDF_NAME

pdfmetrics.registerFont(
    TTFont('DejaVuSans', 'DejaVuSans.ttf'))


def download_shopping_cart(_, request):
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
    pdf.setFont("DejaVuSans", 12)

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
    response['Content-Disposition'] = f'attachment; filename="{PDF_NAME}"'
    return response
