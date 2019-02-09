from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from contacts.models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user have made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry on this property')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        # Send mail

        send_mail(
            'Property Listing Inquiry',
            'There has been an Inquiry for '+ listing + 'Sign into the admin panel for more info',
            'mosesibe@outlook.com',
            [realtor_email, 'mosesibe@outlook.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted, the realtor on this property will reach out to you soon')
        return redirect('/listings/'+listing_id)