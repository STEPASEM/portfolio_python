from django.shortcuts import render

def index(request):
    template_name = 'homepage/index.html'
    title = 'Главная страница ACME'
    promo_product = 'Iron carrot'
    context = {
        'title': title,
        'promo_product': promo_product,
    }
    return render(request, template_name, context)