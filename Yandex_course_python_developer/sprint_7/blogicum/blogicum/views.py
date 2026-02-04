from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class AutoLoginCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)
        # Логиним сразу
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response