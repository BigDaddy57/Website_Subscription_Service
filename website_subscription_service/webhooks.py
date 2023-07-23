# webhooks.py

from django.http import HttpResponse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_htDRQUnvGjWFy3qsxLJ7Rfy06Bj2Jeds'  # your webhook secret

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        # Handle the event based on its type
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object  # contains a stripe.PaymentIntent
            print('PaymentIntent was successful!')
            # Here you might want to lookup the PaymentIntent in your database and mark it as paid
            pass
        
        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            print('PaymentIntent failed!')
            # Here you might want to send an email to the user, log the failure, etc.
            pass
        # Add more event types as per your requirement

        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
