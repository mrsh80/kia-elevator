from django.shortcuts import get_object_or_404, render,redirect
from django.core.paginator import Paginator
from .models import Category, Product
from django.db import models
from .forms import ContactMessageForm
from django.core.cache import cache
from django.http import HttpResponse


def home(request):

    featured_products = Product.objects.filter(
        is_active=True
    ).select_related(
        "category"
    )[:6]

    categories = Category.objects.filter(
        is_active=True
    )

    return render(
        request,
        "home.html",
        {
            "featured_products": featured_products,
            "categories": categories,
        }
    )


def product_list(request):

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    products = Product.objects.filter(
        is_active=True
    ).select_related(
        "category"
    )

    categories = Category.objects.filter(
        is_active=True
    )

    if query:

        products = products.filter(
            models.Q(name__icontains=query)
            | models.Q(short_description__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(category__name__icontains=query)
        )

    if category_slug:

        products = products.filter(
            category__slug=category_slug
        )

    paginator = Paginator(
        products,
        9
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/product_list.html",
        {
            "products": page_obj,
            "page_obj": page_obj,
            "query": query,
            "categories": categories,
            "category_slug": category_slug,
        }
    )

def product_detail(request, slug):

    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True
    )

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product
        }
    )


def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related(
        "category"
    )

    paginator = Paginator(
        products,
        9
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/category_products.html",
        {
            "category": category,
            "products": page_obj,
            "page_obj": page_obj,
        }
    )
def about(request):

    return render(
        request,
        "about.html"
    )
    
def contact(request):

    if request.method == "POST":

        client_ip = request.META.get(
            "REMOTE_ADDR",
            "unknown"
        )

        cache_key = f"contact_form_{client_ip}"

        if cache.get(cache_key):

            form = ContactMessageForm()

            return render(
                request,
                "contact.html",
                {
                    "form": form,
                    "rate_limited": True,
                }
            )

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            form.save()

            cache.set(
                cache_key,
                True,
                60
            )

            request.session["contact_success"] = True

            return redirect("contact")

    else:

        form = ContactMessageForm()

    success = request.session.pop(
        "contact_success",
        False
    )

    return render(
        request,
        "contact.html",
        {
            "form": form,
            "success": success,
        }
    )
def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        "/sitemap.xml"
        )

    content = f"""User-agent: *


            Allow: /

            Disallow: /admin/

            Sitemap: {sitemap_url}"""


    return HttpResponse(
        content,
        content_type="text/plain"
            )
