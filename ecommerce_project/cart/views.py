from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart,CartItem
from shop.models import Product,Category
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def addcart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product,cart=cart,quantity=1)
        cart_item.save()
    return redirect('cart:CartDetails')

def CartDetails(request,total=0,counter=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html', dict(cart_items=cart_items,total_amount=total,counter=counter))

def cart_remove(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_items = CartItem.objects.get(product=product,cart=cart)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('cart:CartDetails')

def car_delete_all(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_items = CartItem.objects.get(product=product,cart=cart)
    cart_items.delete()
    return redirect('cart:CartDetails')