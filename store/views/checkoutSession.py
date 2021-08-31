from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import redirect
import django.views.generic
# for payments
from django.views import View
import stripe
from store.models.orders import Order
from store.models.product import Products
# This is your real test secret API key.
stripe.api_key = settings.STRIP_SECRET_KEY

usr = list()


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        usr.append(request.POST.get("address"))
        usr.append(request.POST.get("number"))
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        customer = request.session.get('customer')
        # print(products)
        newUser = Order.objects.filter(customer_id=customer)
        totalPrice = 0
        productsList = list()
        for product in products:
            totalPrice += product.price
            productsList.append(product)

        # * Removing items from cart
        #request.session['cart'] = {}
        YOUR_DOMAIN = "https://kv.ddns.net"
        if newUser.exists():
            checkout_session = stripe.checkout.Session.create(

                payment_method_types=[

                    'card',
                ],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': totalPrice*100,
                            'product_data': {
                                'name': "Total Amount to pay is",
                                # img
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment',
                cancel_url=YOUR_DOMAIN + '/cart',
            )

        else:
            checkout_session = stripe.checkout.Session.create(

                payment_method_types=[

                    'card',
                ],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': int((totalPrice*100)*0.9),
                            'product_data': {
                                'name': "Total Amount to pay is",
                                # img
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment',
                cancel_url=YOUR_DOMAIN + '/cart',
            )

        return redirect(checkout_session.url, code=303)
