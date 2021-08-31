from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from django.views import View
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
# Create your views here.


class Index(View):

    def post(self, request):
       # print("In Post Function")
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # print('cart' , request.session['cart'])
        return redirect('homepage')  # homepage

    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
   # print("In Store Function")
    data = {}
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        if cache.get(categoryID):
            products = cache.get(categoryID)
        else:
            products = Products.get_all_products_by_categoryid(categoryID)
        # print("In products category cacheing")
            cache.set(categoryID, products)
        # products = Products.get_all_products_by_categoryid(categoryID)
        # cache.set(products, products)
    else:
        if cache.get(products):
            products = cache.get(products)
        else:
            product = Products.get_all_products()
            cache.set(products, product)
        # print("Caching....")
    data["products"] = products
    data['categories'] = categories
    return render(request, 'index.html', data)
