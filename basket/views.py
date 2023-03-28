from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Gadget
from shop.views import menu
from .basket import Basket
from .forms import BasketAddProductForm
from django.views.decorators.http import require_POST


def basket_add(request, product_id):
    basket = Basket(request)
    basket.add(product_id)
    return redirect('list_basket_prod')


def basket_remove(request, product_id):
    basket = Basket(request)
    product_obj = get_object_or_404(Gadget, pk=product_id)
    basket.remove(product_obj)
    return redirect('list_basket_prod')


def basket_info(request):
    context = {}
    context['basket'] = Basket(request)
    context['menu'] = menu
    return render(request, 'basket/detail.html', context)


def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('shop')