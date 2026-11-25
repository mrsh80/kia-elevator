from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Category, Product, ContactMessage
from .forms import ProductForm, CategoryForm


# --------------------------------------------------
# Dashboard Home
# --------------------------------------------------

@staff_member_required(login_url="/admin/login/")
def dashboard_home(request):

    context = {
        "total_products": Product.objects.count(),
        "total_categories": Category.objects.count(),
        "total_messages": ContactMessage.objects.count(),
        "active_products": Product.objects.filter(
            is_active=True
        ).count(),
    }

    return render(request, "dashboard/home.html", context)


# --------------------------------------------------
# Product Management
# --------------------------------------------------

@staff_member_required(login_url="/admin/login/")
@permission_required("core.view_product", login_url="/admin/login/")
def product_list(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(slug__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(technical_specs__icontains=search_query)
        )

    if category_id.isdigit():
        products = products.filter(category_id=category_id)

    if status == "active":
        products = products.filter(is_active=True)

    elif status == "inactive":
        products = products.filter(is_active=False)

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.order_by("name"),
        "search_query": search_query,
        "selected_category": category_id,
        "selected_status": status,
    }

    return render(
        request,
        "dashboard/products/product_list.html",
        context
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.add_product", login_url="/admin/login/")
def product_create(request):

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "محصول جدید با موفقیت ثبت شد.")
            return redirect("dashboard:product_list")

    else:
        form = ProductForm()

    return render(
        request,
        "dashboard/products/product_form.html",
        {
            "form": form,
            "page_title": "افزودن محصول جدید",
            "submit_text": "ثبت محصول",
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.change_product", login_url="/admin/login/")
def product_update(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            messages.success(request, "محصول با موفقیت ویرایش شد.")
            return redirect("dashboard:product_list")

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "dashboard/products/product_form.html",
        {
            "form": form,
            "page_title": "ویرایش محصول",
            "submit_text": "ذخیره تغییرات",
            "product": product,
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.delete_product", login_url="/admin/login/")
def product_delete(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "محصول با موفقیت حذف شد.")
        return redirect("dashboard:product_list")

    return render(
        request,
        "dashboard/products/product_confirm_delete.html",
        {"product": product}
    )


# --------------------------------------------------
# Category Management
# --------------------------------------------------

@staff_member_required(login_url="/admin/login/")
@permission_required("core.view_category", login_url="/admin/login/")
def category_list(request):

    categories = Category.objects.all().order_by("-created_at")

    search_query = request.GET.get("q", "").strip()

    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query)
            | Q(slug__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    paginator = Paginator(categories, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "dashboard/categories/category_list.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.add_category", login_url="/admin/login/")
def category_create(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "دسته‌بندی با موفقیت ایجاد شد.")
            return redirect("dashboard:category_list")

    else:
        form = CategoryForm()

    return render(
        request,
        "dashboard/categories/category_form.html",
        {
            "form": form,
            "page_title": "افزودن دسته‌بندی",
            "submit_text": "ثبت دسته‌بندی",
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.change_category", login_url="/admin/login/")
def category_update(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "دسته‌بندی با موفقیت ویرایش شد.")
            return redirect("dashboard:category_list")

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "dashboard/categories/category_form.html",
        {
            "form": form,
            "page_title": "ویرایش دسته‌بندی",
            "submit_text": "ذخیره تغییرات",
            "category": category,
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.delete_category", login_url="/admin/login/")
def category_delete(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        if Product.objects.filter(category=category).exists():
            messages.error(
                request,
                "این دسته‌بندی دارای محصول است و فعلاً قابل حذف نیست."
            )
            return redirect("dashboard:category_list")

        category.delete()

        messages.success(request, "دسته‌بندی با موفقیت حذف شد.")
        return redirect("dashboard:category_list")

    return render(
        request,
        "dashboard/categories/category_confirm_delete.html",
        {"category": category}
    )


# --------------------------------------------------
# Contact Messages Management
# --------------------------------------------------

@staff_member_required(login_url="/admin/login/")
@permission_required("core.view_contactmessage", login_url="/admin/login/")
def message_list(request):

    message_list = ContactMessage.objects.all().order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")

    if search_query:
        message_list = message_list.filter(
            Q(name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(message__icontains=search_query)
        )

    if status == "unread":
        message_list = message_list.filter(is_read=False)

    elif status == "read":
        message_list = message_list.filter(is_read=True)

    paginator = Paginator(message_list, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "dashboard/messages/message_list.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "selected_status": status,
            "unread_count": ContactMessage.objects.filter(
                is_read=False
            ).count(),
        }
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.view_contactmessage", login_url="/admin/login/")
def message_detail(request, pk):

    contact_message = get_object_or_404(ContactMessage, pk=pk)

    if not contact_message.is_read:
        contact_message.is_read = True
        contact_message.save(update_fields=["is_read"])

    return render(
        request,
        "dashboard/messages/message_detail.html",
        {"contact_message": contact_message}
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.delete_contactmessage", login_url="/admin/login/")
def message_delete(request, pk):

    contact_message = get_object_or_404(ContactMessage, pk=pk)

    if request.method == "POST":
        contact_message.delete()
        messages.success(request, "پیام با موفقیت حذف شد.")
        return redirect("dashboard:message_list")

    return render(
        request,
        "dashboard/messages/message_confirm_delete.html",
        {"contact_message": contact_message}
    )


@staff_member_required(login_url="/admin/login/")
@permission_required("core.change_contactmessage", login_url="/admin/login/")
def message_mark_unread(request, pk):

    if request.method == "POST":
        contact_message = get_object_or_404(ContactMessage, pk=pk)

        contact_message.is_read = False
        contact_message.save(update_fields=["is_read"])

        messages.success(request, "پیام به‌عنوان خوانده‌نشده علامت‌گذاری شد.")

    return redirect("dashboard:message_list")