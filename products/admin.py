from django.contrib import admin
from django import forms
from .models import Product


class ProductAdminForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False,
        label='Image URL',
        help_text='Paste a direct image URL (from Cloudinary, Pinterest, etc.)',
        widget=forms.TextInput(attrs={'style': 'width: 500px;', 'placeholder': 'https://...'})
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image_url'].initial = self.instance.image

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            instance.image = image_url
        if commit:
            instance.save()
        return instance


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    exclude = ['image']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
