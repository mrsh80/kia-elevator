from django.db import models
from .validators import (
    validate_image_size,
    validate_image_extension,
    validate_image_content,
)
from .image_utils import optimize_image


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="نام دسته‌بندی"
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="اسلاگ"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "دسته‌بندی"

        verbose_name_plural = "دسته‌بندی‌ها"

        ordering = ["name"]


    def __str__(self):
        return self.name
    
class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته‌بندی"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="نام محصول"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="اسلاگ"
    )

    short_description = models.CharField(
        max_length=300,
        verbose_name="توضیح کوتاه"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    image = models.ImageField(
    upload_to="products/",
    validators=[
        validate_image_size,
        validate_image_extension,
        validate_image_content,
    ],
    verbose_name="تصویر محصول"
    )

    technical_specs = models.TextField(
        blank=True,
        verbose_name="مشخصات فنی"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "محصول"

        verbose_name_plural = "محصولات"

        ordering = ["-created_at"]
    def save(self, *args, **kwargs):

        image_changed = False

        if self.pk and self.image:

            old_product = Product.objects.get(pk=self.pk)

            if old_product.image.name != self.image.name:
                image_changed = True

        elif self.image:

            image_changed = True

        if image_changed:

            optimized_image = optimize_image(
                self.image
            )

            self.image.save(
                self.image.name,
                optimized_image,
                save=False
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="نام"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="شماره تماس"
    )

    email = models.EmailField(
        blank=True,
        verbose_name="ایمیل"
    )

    subject = models.CharField(
        max_length=200,
        verbose_name="موضوع"
    )

    message = models.TextField(
        verbose_name="پیام"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="خوانده شده"
    )


    class Meta:

        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

        ordering = ["-created_at"]


    def __str__(self):

        return f"{self.name} - {self.subject}"