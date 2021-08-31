from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        # tempOrder=Order.objects.none()
        tempOrders=list()
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        newUser=Order.objects.filter(customer_id=customer)
        #print(customer)
        #print(newUser)
        totalPrice=0
        for product in products:
            
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            totalPrice+=product.price
            tempOrders.append(order)
            #order.save()
        #request.session['cart'] = {}
        if newUser.exists():
            print("Not new user")
            return render(request,"payment-checkout.html",context={"data":tempOrders,"total":totalPrice})
        else:
          print("New User")
          return render(request,"payment-checkout.html",context={"data":tempOrders,"total":int(totalPrice*0.9),"message":"Since you are new user we are willing to give you 10% discount"})

