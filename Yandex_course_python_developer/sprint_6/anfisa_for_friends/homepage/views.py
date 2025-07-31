from django.shortcuts import render

from ice_cream.models import IceCream

def index(request):
    template_name = 'homepage/index.html'
    ice_cream_list = IceCream.objects.values(
        'id', 'title', 'description'
    ).filter(
        is_published=True, is_on_main=True  # Два в одном!
    ).order_by('title')[0:3]
    # Полученный из БД QuerySet передаём в словарь контекста:
    context = {
        'ice_cream_list': ice_cream_list,
    }
    return render(request, template_name, context)
