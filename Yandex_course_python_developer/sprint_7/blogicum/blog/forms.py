from django import forms
from .models import Post, Category, Location, Comment


class PostForm(forms.ModelForm):
    category_text = forms.CharField(
        max_length=256,
        required=False,
        label='Категория',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите категорию'
        })
    )

    location_text = forms.CharField(
        max_length=256,
        required=False,
        label='Местоположение',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите местоположение'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Предзаполняем текущие значения при редактировании
        if self.instance and self.instance.pk:
            if self.instance.category:
                self.fields['category_text'].initial = self.instance.category.title
            if self.instance.location:
                self.fields['location_text'].initial = self.instance.location.name

    def save(self, commit=True):
        post = super().save(commit=False)

        from django.utils import timezone
        post.pub_date = timezone.now()

        # Обработка категории
        category_text = self.cleaned_data.get('category_text')
        if category_text:
            category, created = Category.objects.get_or_create(
                title=category_text,
                defaults={
                    'slug': category_text.lower().replace(' ', '-')[:64],
                    'description': f'Категория {category_text}',
                    'is_published': True
                }
            )
            post.category = category
        else:
            post.category = None

        # Обработка локации
        location_text = self.cleaned_data.get('location_text')
        if location_text:
            location, created = Location.objects.get_or_create(
                name=location_text,
                defaults={'is_published': True}
            )
            post.location = location
        else:
            post.location = None

        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите ваш комментарий...'
            })
        }
        labels = {
            'text': 'Комментарий'
        }
        help_texts = {
            'text': 'Напишите ваш комментарий к посту'
        }