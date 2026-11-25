from django import forms

from core.models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "image",
            "technical_specs",
            "is_active",
        ]

        widgets = {
            "category": forms.Select(attrs={
                "class": "form-control",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام محصول",
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "product-slug",
                "dir": "ltr",
            }),
            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "technical_specs": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-checkbox",
            }),
        }

        labels = {
            "category": "دسته‌بندی",
            "name": "نام محصول",
            "slug": "شناسه URL",
            "short_description": "توضیح کوتاه",
            "description": "توضیحات کامل",
            "image": "تصویر محصول",
            "technical_specs": "مشخصات فنی",
            "is_active": "محصول فعال باشد",
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "slug",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام دسته‌بندی",
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "category-slug",
                "dir": "ltr",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "توضیحات دسته‌بندی",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-checkbox",
            }),
        }

        labels = {
            "name": "نام دسته‌بندی",
            "slug": "شناسه URL",
            "description": "توضیحات",
            "is_active": "دسته‌بندی فعال باشد",
        }