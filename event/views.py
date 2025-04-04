import base64
from datetime import datetime
import requests
import os
import pprint
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.http import HttpResponse, request, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from Scheduler import settings
from event.forms import RegisterForm, AccommodationForm, FoodForm, PaymentForm, ContactForms


# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def accommodation(request):
    return render(request,'accommodation.html')
def food(request):
    return render(request,'food.html')
def happyclients(request):
    return render(request,'happyclients.html')
def contact(request):
    form = ContactForms()
    if request.method == "POST":
        form = ContactForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Construct the email content
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send email to admin
            send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, ['tonnysafari3@gmail.com'])

            return redirect('succesful')  # Redirect to a success page
    else:
        form = ContactForms()

    return render(request, "contact.html", {"form": form})

@login_required
def booking(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)  # Create the model instance but don't save yet
            accommodation.user = request.user  # Set the user
            accommodation.save()  # Now save the instance
            return redirect('booking')
    else:
        form = AccommodationForm()
    return render(request, 'booking.html', {'form': form})
@login_required
def order(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)  # Create the model instance but don't save yet
            food.user = request.user  # Set the user
            food.save()  # Now save the instance
            return redirect('oder')
    else:
        form = FoodForm()
    return render(request, 'order.html', {'form': form})



def login_view(request):
    pass

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
# def
def logout_view(request):
    logout(request)
    return redirect('login')
def payment_form(request):
    return render(request,'payment_form.html')

def payment_processing(request):
 if request.method == 'POST':
    form = PaymentForm(request.POST)
    if form.is_valid():
        # Get the phone number and amount from the form
        phone_number = form.cleaned_data['phone_number']
        amount = form.cleaned_data['amount']

        # Convert amount to integer (in cents)
        amount_in_cents = int(amount * 1)  # Convert amount to cents

        cl = MpesaClient()
        account_reference = '@Toneyz'
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment'
        response = cl.stk_push(phone_number, amount_in_cents, account_reference, transaction_desc, callback_url)
        return HttpResponse(response)
 else:
    form = PaymentForm()

 return render(request, 'payment_processing.html', {'form': form})