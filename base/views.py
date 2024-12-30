import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Visitor
from .forms import VisitorForm

import qrcode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from VisitorEntrySystem.settings import DEFAULT_FROM_EMAIL, SITE_URL


def generate_qr(request, user):
    if request.method == 'POST':
        link = f'{SITE_URL}/profile/{user.pk}/'
        user_email = user.email

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save QR code to a file-like object
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_image_data = buffer.getvalue()

        # Send QR code via email
        email = EmailMessage(
            subject='Your QR Code',
            body='Here is your QR Code. Please find it attached.',
            from_email=DEFAULT_FROM_EMAIL,  # Replace with your email
            to=[user_email],
        )
        # Attach QR code image
        email.attach('qr_code.png', qr_image_data, 'image/png')

        # Send the email
    return email.send()


def registerPage(request):
    """Handle user registration and QR code generation/email."""
    form = VisitorForm()

    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            generate_qr(request, user)
            return redirect('registration-complete')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def userProfile(request, pk):
    """Display the user's profile."""
    try:
        user = Visitor.objects.get(id=pk)
        return render(request, 'base/profile.html', {'user': user})
    except Visitor.DoesNotExist:
        return render(request, 'base/access_denied.html', status=404)
    

def home(request):
    return redirect('register')


def registration_complete(request):
    return render(request, 'base/register_complete.html', status=201)