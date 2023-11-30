from .models import Category


def categories(request):
    context = {
        'categories': Category.objects.all()
    }
    return context
