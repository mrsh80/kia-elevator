from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Product

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "product_list",
            "about",
            "contact",
        ]

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(
            is_active=True
        ).select_related("category")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "product_detail",
            kwargs={"slug": obj.slug}
        )

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7


    def items(self):
        return Category.objects.filter(
            is_active=True
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "category_products",
            kwargs={"slug": obj.slug}
        )

