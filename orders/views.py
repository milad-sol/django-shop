from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from .forms import CartAddForm

from product.models import Product


# Create your views here.


class CartView(View):

    def get(self, request):
        return render(request, 'orders/cart.html')


class AddToCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product=product, quantity=form.cleaned_data['quantity'])
        return redirect('orders:cart')
