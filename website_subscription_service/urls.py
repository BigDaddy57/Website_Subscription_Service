"""
URL configuration for website_subscription_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from subscription import views
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from subscription.views import comment_view, login_view
from subscription.views import home_view
from django.urls import include
from subscription.views import learning_resources
from .webhooks import stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('', home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('comments/', views.comment_view, name='comment_view'),
    path('legal/', include('legal.urls')),
    path('learning_resources/', learning_resources, name='learning_resources'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('stripe-webhook/', stripe_webhook, name='stripe_webhook'),

]


