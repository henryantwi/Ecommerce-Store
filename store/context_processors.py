from .models import Category


def categories(request) -> dict:
    context = {
        'categories': Category.objects.all()
    }
    return context
