from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CartAddForm
from .cart import Cart
from product.models import Product


# Create your views here.


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class AddToCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product=product, quantity=form.cleaned_data['quantity'])
        return redirect('orders:cart')


class RemoveFromCartView(View):
    def get (self, request, product_id):
       cart = Cart(request)
       product = get_object_or_404(Product, id=product_id)
       cart.remove(product)
       return redirect('orders:cart')