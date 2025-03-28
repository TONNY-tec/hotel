import base64
from datetime import datetime
import requests
import os

from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.http import HttpResponse, request, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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

def get_access_token():
    consumer_key = 'GXrNmTPFPsGz7YfPVNnKPzefcDRKxywenpdO3pIpGvw494GO'
    consumer_secret = 'tuTDN0werDZfoINHGjlqse0f1phHIk2GQ3vIRm0bkw08XqCyFGsCfNbQ04xaytAn'
    api_url = f"{'https://sandbox.safaricom.co.ke'}/oauth/v1/generate?grant_type=client_credentials"
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        access_token = data.get("access_token")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error generating access token: {e}")
        return None

def initiate_stk_push(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = int(form.cleaned_data['amount'])  # Amount must be an integer

            access_token = get_access_token()
            if not access_token:
                return render(request, 'payment_error.html', {'error': 'Failed to get access token'})

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(( 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' + timestamp).encode()).decode()
            api_url = f"{'https://sandbox.safaricom.co.ke'}/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": f"Bearer {access_token}"}
            payload = {
                "BusinessShortCode": 174379,
                "Password": password,  # Use the generated password
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayOnline",
                "Amount": amount,
                "PartyA": f"254{phone_number.lstrip('0')}",  # Customer's phone number (format: 2547XXXXXXXX)
                "PartyB": 174379,  # Use your business shortcode here
                "PhoneNumber": f"254{phone_number.lstrip('0')}",  # Customer's phone number
                "CallBackURL": request.build_absolute_uri('/event/stk-callback/'), # Ensure this URL is correctly configured
                "AccountReference": "Payment for your order",
                "TransactionDesc": "Payment for your order"
            }

            try:
                response = requests.post(api_url, headers=headers, json=payload, verify=False)
                response.raise_for_status()
                data = response.json()
                print(f"STK Push Response: {data}")
                return render(request, 'payment_processing.html', {'response_data': data})
            except requests.exceptions.RequestException as e:
                print(f"Error initiating STK push: {e}")
                return render(request, 'payment_error.html', {'error': f'Failed to initiate payment: {e}'})
        else:
            return render(request, 'payment_form.html', {'form': form})
    else:
        form = PaymentForm()
        return render(request, 'payment_form.html', {'form': form})

@csrf_exempt
def stk_push_callback(request):
    if request.method == 'POST':
        try:
            callback_data = request.body.decode('utf-8')
            import json
            callback_json = json.loads(callback_data)
            print(f"STK Push Callback Received: {callback_json}")

            # Process the callback data here to update your order status
            # Example of accessing data:
            # result_code = callback_json.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            # merchant_request_id = callback_json.get('Body', {}).get('stkCallback', {}).get('MerchantRequestID')

            # You should acknowledge receipt with a 200 OK response
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})
        except Exception as e:
            print(f"Error processing STK push callback: {e}")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Failed'})
    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid Request'})