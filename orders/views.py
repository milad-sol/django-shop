from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CartAddForm, CouponApplyForm
from .cart import Cart
from product.models import Product
from .models import Order, OrderItem, Coupon


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
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order_id=order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = self.form_class()
        return render(request, 'orders/order.html', {'order': order, 'form': form})


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()
        return redirect('orders:order_detail', order_id=order.id)


class OrderApplyView(View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)

            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon is expired or invalid', 'danger')
                return redirect('orders:order_detail', order_id=order_id)

            order = get_object_or_404(Order, id=order_id)
            order.discount = coupon.discount
            order.save()
            messages.success(request, 'you have applied this coupon', 'success')
        return redirect('orders:order_detail', order_id=order_id)
