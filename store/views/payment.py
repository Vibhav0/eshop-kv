from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order
from store.views.checkoutSession import usr

# *When payment is done
def paymentDone(request):
    #address = request.POST.get('address')
    #phone = request.POST.get('phone')
    #address = "301 RoseWood, 21 JumpStreet, Mumbai"
    #phone = "7875028239"
    # tempOrder=Order.objects.none()
    customer = request.session.get('customer')
    cart = request.session.get('cart')
    products = Products.get_products_by_id(list(cart.keys()))
    # print(cart)
    totalPrice = 0
    for product in products:

        order = Order(customer=Customer(id=customer),
                      product=product,
                      price=product.price,
                      address=usr[0],
                      phone=usr[1],
                      quantity=cart.get(str(product.id)))
        order.save()
    request.session['cart'] = {}

    return redirect("/orders")
