from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import CartItem, Cart
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal as D
# Create your views here.


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'total': human_format(float(total)),
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': human_format(float(total * D("0.02"))),
        'final_total': human_format(float(total * D("1.18")))
    }

    return render(request, 'store/cart.html', context)


def add_cart(request, product_id):
    color = request.GET['color']
    size = request.GET['size']

    return HttpResponse(color + ' ' + size)
    exit()

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_get_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
    cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
  cart = Cart.objects.get(cart_id = _get_cart_id(request))
  product = get_object_or_404(Product, id = product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  if cart_item.quantity  > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
  return redirect('cart')


def remove_cart_item(request, product_id):
  cart = Cart.objects.get(cart_id = _get_cart_id(request))
  product = get_object_or_404(Product, id = product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  cart_item.delete()
  return redirect('cart')