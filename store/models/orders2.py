from django.db import models
from .product import Products
from .customer import Customer
import datetime


class Order2(models.Model):
    orderId=
    fullName=
    email=
    address=
    city=
    state=
    pinCode=
    nameOnCard=
    cardNumber=
    exp


    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order2.objects.filter(customer=customer_id).order_by('-date')

