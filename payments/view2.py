from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import redirect

#for payments

import stripe
# This is your real test secret API key.
stripe.api_key = settings.STRIP_SECRET_KEY

class CreateCheckoutSessionView(generic.View):
      def post(self, *args, **kwargs):
        
        # host = self.request.get_host()
        YOUR_DOMAIN = "http://127.0.0.1:8000"
           checkout_session = stripe.checkout.Session.create(
            payment_method_types=[
              'card',
            ],
            line_items=[
                {
                    'price_data':{
                     'currency': 'inr',
                     'unit_amount': 1000;
                     'product_data':{
                        'name': 'codepiep order',
                        #img
                     }
                    }
                    'quantity': 1;
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        
        return redirect(checkout_session.url, code=303)


        def paymentSuccess(request):
          context={
           'payment_status':'success'
          }
          return render(request, 'store/confirmation.html', context)

        def paymentCancel(request):
          context=
          {
            'payment_status':'cancel'
          }

          return render(request,"store/confirmation.html",context)