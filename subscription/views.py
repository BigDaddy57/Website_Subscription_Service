import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Feedback
from .models import Subscription
from django.contrib.auth.decorators import login_required
from subscription import views
from django.contrib.auth.models import User
from .models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
import logging
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

def landing_page(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'landing_page.html')

@login_required
def home_view(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_checkout_session(request):
    domain_url = 'http://localhost:8000/'  # replace with your domain
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + reverse('success'),
            cancel_url=domain_url + reverse('cancelled'),
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': 'price_1NQibrDcLUHrpFpKCzIyPOAy',  # replace with the Price ID
                    'quantity': 1,
                }
            ]
        )
        return render(request, 'checkout.html', context={'session_id': checkout_session['id'], 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
    except Exception as e:
        print(e)  # print the exception message
        return HttpResponse(str(e), status=403)

@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def cancelled(request):
    try:
        # Get the user's subscription
        subscription = Subscription.objects.get(user=request.user)

        # Get the Stripe subscription ID
        stripe_subscription_id = subscription.stripe_subscription_id

        # Cancel the subscription
        stripe.Subscription.delete(stripe_subscription_id)

        # Update the user's subscription status in your database
        subscription.status = 'cancelled'
        subscription.save()

    except Subscription.DoesNotExist:
        # Handle case where user does not have a subscription
        messages.error(request, "No active subscription found.")
    except Exception as e:
        # Handle other exceptions
        messages.error(request, str(e))

    return render(request, 'cancelled.html')

def check_subscription(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        subscription = Subscription.objects.filter(user=request.user, status='active').exists()
        if subscription:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('subscribe_page')
    return _wrapped_view_func

@login_required
def terms_and_conditions(request):
    return render(request, 'legal/terms_and_conditions.html')

@login_required
def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')

@login_required
def learning_resources(request):
    resources = [
        'Glossary of Stock Market Terms',
        'Practice Your Skills with MarketWatch Virtual Game',
        'Get Free Stocks with My Webull Referral Code',
        '9 Expert-Recommended Educational Resources For Newcomers To The Stock Market',
        'The Best Online Stock Trading Classes of 2023',
        '10 Great Ways to Learn Stock Trading in 2023',
        # Add more resources as needed
    ]
    return render(request, 'learning_resources.html', {'resources': resources})

@login_required
def comment_view(request):
    if request.method == 'POST':
        # Retrieve the comment text from the form
        comment_text = request.POST.get('comment_text')

        # Only create a Comment object if comment_text is not empty
        if comment_text:
            # Create a new Comment object and save it to the database
            comment = Comment(comment_text=comment_text, user=request.user)
            comment.save()

        # Check if the feedback form was submitted
        feedback_text = request.POST.get('feedback_text')
        if feedback_text:
            # Create a new Feedback object and save it to the database
            feedback = Feedback(user=request.user, feedback_text=feedback_text)
            feedback.save()

        # Redirect to the same page after the comment is submitted
        return redirect(request.path)

    else:
        # Retrieve all the comments and feedbacks from the database
        comments = Comment.objects.all()
        feedbacks = Feedback.objects.all()

        # Render the comment section template with the comments and feedbacks
        return render(request, 'comment_section.html', {'comments': comments, 'feedbacks': feedbacks})

@login_required
def delete_comment(request, comment_id):
    # Get the comment object
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    # Check if the current user is the author of the comment
    if request.user == comment.user:
        # Delete the comment
        comment.delete()

    # Redirect to the comments page
    return redirect('comment_view')

@login_required
def delete_feedback(request, feedback_id):
    # Get the feedback object
    feedback = get_object_or_404(Feedback, id=feedback_id, user=request.user)

    # Check if the current user is the author of the feedback
    if request.user == feedback.user:
        # Delete the feedback
        feedback.delete()

    # Redirect to the comments page
    return redirect('comment_view')
