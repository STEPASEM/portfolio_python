from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday
from .utils import calculate_birthday_countdown



class BirthdayListView(ListView):
    model = Birthday
    template_name = 'birthday/list.html'
    context_object_name = 'birthdays'
    paginate_by = 3

class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:create')

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)

class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )
        return context

@login_required
def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    if instance:
        birthday_countdown = calculate_birthday_countdown(instance.birthday)
        context['birthday_countdown'] = birthday_countdown
    if form.is_valid():
        action = request.POST.get('action')
        if action == 'delete' and instance:
            form.instance.delete()
            return redirect('birthday:list')
        elif action == 'save':
            form.save()
            birthday_countdown = calculate_birthday_countdown(form.cleaned_data['birthday'])
            context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)

@login_required
def add_comment(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        congratulation.author = request.user
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)
