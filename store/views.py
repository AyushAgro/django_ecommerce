from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _get_cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    all_categories = Category.objects.all()
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        products_count = products.count()
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        products = paginator.get_page(page)
    context = {
        'products': products,
        'products_count': products_count,
        'Categories': all_categories
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_get_cart_id(request), product=single_product)
    except Exception as e:
        print(e)

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    products_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains = keyword) | Q(product_name__icontains = keyword)
            )
            products_count = products.count()
    context = {
    'products': products,
    'products_count': products_count,
    }
    print(context)
    return render(request, 'store/store.html',context)
