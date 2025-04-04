from django.urls import path
from django.contrib.auth import views as auth_views
from event import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('food/', views.food, name='food'),
    path('happyclients/', views.happyclients, name='happyclients'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('order/', views.order, name='order'),
    path('payment_processing/', views.payment_processing, name='payment_processing'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('payment_form/',views.payment_form, name='payment_form'),
]