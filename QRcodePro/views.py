#------------------------------------------------Modules----------------------------------------------------#
import json
import base64
import qrcode
from io import BytesIO
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageOps
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request,'QRcodePro/index.html')


#------------------------------------------------Generate QR For views-------------------------------------------#
from PIL import Image, ImageDraw, ImageOps

def embed_logo_on_qr(img, logo_file, logo_shape, logo_corner):
    """
    Embeds the uploaded logo onto the QR code image.
    :param img: The QR code image
    :param logo_file: The uploaded logo file
    :param logo_shape: The shape of the logo ('circle' or 'square')
    :param logo_corner: The corner type for square logos ('rounded' or 'sharp')
    :return: The QR code image with the embedded logo
    """
    logo = Image.open(logo_file)
    qr_size = min(img.size)
    max_logo_size = qr_size // 5  # Logo should be no larger than 20% of the QR code's size
    logo_size = min(max_logo_size, min(logo.size))  # Resize to fit logo dimensions

    # Resize logo
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Create mask for logo shape
    mask = Image.new('L', (logo_size, logo_size), 0)
    draw = ImageDraw.Draw(mask)

    if logo_shape == 'circle':
        draw.ellipse((0, 0, logo_size, logo_size), fill=255)
        logo = ImageOps.fit(logo, (logo_size, logo_size), centering=(0.5, 0.5))
        logo.putalpha(mask)

    elif logo_shape == 'square':
        if logo_corner == 'rounded':
            radius = logo_size // 5  # Adjust radius as a proportion of the logo size
            draw.rounded_rectangle((0, 0, logo_size, logo_size), radius, fill=255)
        else:  # Sharp corners
            draw.rectangle((0, 0, logo_size, logo_size), fill=255)
        logo.putalpha(mask)

    # Embed logo at the center of the QR code
    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
    img.paste(logo, pos, logo)

    return img



#-----------------------------------------------Text to QR----------------------------------------------------------#


def text(request):
    # Default data for GET requests
    data = {
        'type': 'Text'
    }

    if request.method == 'POST':
        text_content = request.POST.get('text_content')
        fill_color = request.POST.get('fill_color')
        background_color = request.POST.get('background_color')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(text_content)
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        # Process logo if uploaded
        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)
        
        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)
    
    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)


#-----------------------------------------------------Email to QR-----------------------------------------------------#

def email(request):
    # Default data for GET requests
    data = {
        'type': 'Email'
    }

    if request.method == 'POST':
        email_address = request.POST.get('email_address')  # Get email input from the form
        subject = request.POST.get('subject', '')  # Default to empty if not provided
        body = request.POST.get('body', '')  # Default to empty if not provided
        fill_color = request.POST.get('fill_color')
        background_color = request.POST.get('background_color')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

      

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        email_content = f"mailto:{email_address}?subject={subject}&body={body}"
        qr.add_data(email_content)  # Add email content to the QR code
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)

    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)


#------------------------------------------------------URL to QR---------------------------------------------------#
def url(request):
    # Default data for GET requests
    data = {
        'type': 'URL'
    }

    if request.method == 'POST':
        url_content = request.POST.get('url')  # Get URL input from the form
        fill_color = request.POST.get('fill_color')
        background_color = request.POST.get('background_color')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        print("Logo  :",logo_file)

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(url_content)  # Add URL content to the QR code
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)
    
    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)



#-----------------------------------------------------Location to QR-----------------------------------------------#

def location(request):
    # Default data for GET requests
    data = {
        'type': 'Location'
    }

    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state', '')
        country = request.POST.get('country')

        fill_color = request.POST.get('fill_color', '#000000')
        background_color = request.POST.get('background_color', '#ffffff')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        # Construct Google Maps URL
        location_url = f"https://www.google.com/maps/search/?api=1&query={street_address}, {city}, {state}, {country}"

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(location_url)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)

    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)


#----------------------------------------------------WhatsApp to QR----------------------------------------------------#
def whatsapp(request):
    # Default data for GET requests
    data = {
        'type': 'WhatsApp'
    }

    if request.method == 'POST':
        whatsapp_number = request.POST.get('whatsapp_number')
        default_message = request.POST.get('default_message', '')

        fill_color = request.POST.get('fill_color', '#000000')
        background_color = request.POST.get('background_color', '#ffffff')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        # Construct WhatsApp URL
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={default_message}"

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(whatsapp_url)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)

    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)


#-------------------------------------------------VCard to QR---------------------------------------------------------#
def vcard(request):
    # Default data for GET requests
    data = {
        'type': 'VCard'
    }

    if request.method == 'POST':
        vcard_name = request.POST.get('vcard_name')
        vcard_phone = request.POST.get('vcard_phone')
        vcard_email = request.POST.get('vcard_email')
        vcard_organization = request.POST.get('vcard_organization')
        vcard_title = request.POST.get('vcard_title')
        vcard_address_street = request.POST.get('vcard_address_street')
        vcard_address_city = request.POST.get('vcard_address_city')
        vcard_address_state = request.POST.get('vcard_address_state')
        vcard_address_country = request.POST.get('vcard_address_country')
        vcard_website = request.POST.get('vcard_website')

        fill_color = request.POST.get('fill_color', '#000000')
        background_color = request.POST.get('background_color', '#ffffff')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        # Construct VCard content
        vcard_content = f"""
        BEGIN:VCARD
        VERSION:3.0
        FN:{vcard_name}
        TEL:{vcard_phone}
        EMAIL:{vcard_email}
        ORG:{vcard_organization}
        TITLE:{vcard_title}
        ADR:;;{vcard_address_street};{vcard_address_city};{vcard_address_state};;{vcard_address_country}
        URL:{vcard_website}
        END:VCARD
        """

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(vcard_content.strip())
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)

    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)



#------------------------------------------------WiFi to QR-------------------------------------------------------------#
def wifi(request):
    # Default data for GET requests
    data = {
        'type': 'WiFi'
    }

    if request.method == 'POST':
        wifi_ssid = request.POST.get('wifi_ssid')  # Get Wi-Fi SSID from form
        encryption = request.POST.get('encryption')  # Get encryption type (WPA, WEP, nopass)
        wifi_password = request.POST.get('wifi_password')  # Get Wi-Fi password if applicable
        fill_color = request.POST.get('fill_color')  # Get QR code fill color
        background_color = request.POST.get('background_color')  # Get QR code background color
        logo_file = request.FILES.get('logo')  # Get uploaded logo if any
        logo_shape = request.POST.get('logo_shape')  # Get logo shape (circle/square)
        logo_corner = request.POST.get('logo_corner')  # Get logo corner style (sharp/rounded)

        # Prepare Wi-Fi format for QR code
        wifi_data = f"WIFI:S:{wifi_ssid};T:{encryption};"
        if encryption != 'nopass':
            wifi_data += f"P:{wifi_password};"
        wifi_data += ";"

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(wifi_data)
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        data['qr_code'] = img_str
        # Render the QR code download page
        return render(request, 'QRcodePro/downloadQR.html', data)
    
    # Render the QR code form page if not a POST request
    return render(request, 'QRcodePro/qrForm.html', data)
  



#--------------------------------------------------Call to QR---------------------------------------------------------#
def call(request):
    data={
        
    'type':'Call'
    }
    if request.method == 'POST':
        # Get phone number and customization inputs from the form
        phone_number = request.POST.get('phone_number')
        fill_color = request.POST.get('fill_color')
        background_color = request.POST.get('background_color')
        logo_file = request.FILES.get('logo')
        logo_shape = request.POST.get('logo_shape')
        logo_corner = request.POST.get('logo_corner')

        # Construct the telephone link format for QR code
        tel_data = f"tel:{phone_number}"

        # Generate QR code with high error correction level
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(tel_data)  # Add phone number in "tel:" format to the QR code
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

        if logo_file:
            img = embed_logo_on_qr(img, logo_file, logo_shape, logo_corner)

        # Save QR code to buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Pass generated QR code to template
        data['qr_code'] = img_str
        return render(request, 'QRcodePro/downloadQR.html', data)

    return render(request,'QRcodePro/qrForm.html',data)



#------------------------------------------------------Api---------------------------------------------------------------#
def api_documentation(request):
    return render(request,'QRcodePro/apiDocumentation.html')

def api_logoEncodingDecoding(request):
    return render(request,'QRcodePro/api_logoEncodingDecoding.html')


@csrf_exempt
def api_generate_qr(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            
            qr_type = data.get('type')
            fill_color = data.get('fill_color', '#000000')
            background_color = data.get('background_color', '#FFFFFF')
            logo_shape = data.get('logo_shape', 'circle')
            logo_corner = data.get('logo_corner', 'sharp')
            logo_file = data.get('logo')  # This will need special handling for file uploads

            # Initialize QR code data
            response_data = {'status': 'fail', 'qr_code': ''}

            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )

            # Handle different QR code types
            if qr_type == 'text':
                text_content = data.get('text_content')
                if not text_content:
                    return JsonResponse({'status': 'fail', 'message': 'Text content is required for type "text"'}, status=400)
                qr.add_data(text_content)

            elif qr_type == 'email':
                email_address = data.get('email_address')  # Get email input from the form
                subject = data.get('subject', '')  # Default to empty if not provided
                body = data.get('body', '') 
                url_content = data.get('url_content')
                if not email_address:
                    return JsonResponse({'status': 'fail', 'message': 'Email content is required for type "url"'}, status=400)
                email_content = f"mailto:{email_address}?subject={subject}&body={body}"
                qr.add_data(email_content)
            elif qr_type == 'url':
                url_content = data.get('url_content')
                if not url_content:
                    return JsonResponse({'status': 'fail', 'message': 'URL content is required for type "url"'}, status=400)
                qr.add_data(url_content)
            
            elif qr_type == 'location':
                street_address = data.get('street_address')
                city = data.get('city')
                state = data.get('state')
                country = data.get('country')
                if not (street_address and city and state and country):
                    return JsonResponse({'status': 'fail', 'message': 'Complete location details are required'}, status=400)
                location_content = f"{street_address}, {city}, {state}, {country}"
                qr.add_data(location_content)
            
            elif qr_type == 'whatsapp':
                whatsapp_number = data.get('whatsapp_number')
                if not whatsapp_number:
                    return JsonResponse({'status': 'fail', 'message': 'WhatsApp number is required'}, status=400)
                default_message = data.get('default_message', '')
                whatsapp_content = f"tel:{whatsapp_number}?text={default_message}"
                qr.add_data(whatsapp_content)
            
            elif qr_type == 'vcard':
                vcard_data = {
                    "name": data.get('vcard_name'),
                    "phone": data.get('vcard_phone'),
                    "email": data.get('vcard_email'),
                    "organization": data.get('vcard_organization'),
                    "title": data.get('vcard_title'),
                    "address_street": data.get('vcard_address_street'),
                    "address_city": data.get('vcard_address_city'),
                    "address_state": data.get('vcard_address_state'),
                    "address_country": data.get('vcard_address_country'),
                    "website": data.get('vcard_website')
                }
                if not any(vcard_data.values()):
                    return JsonResponse({'status': 'fail', 'message': 'VCard data is required'}, status=400)
                vcard_content = '\n'.join([f"{key}: {value}" for key, value in vcard_data.items() if value])
                qr.add_data(vcard_content)
            
            elif qr_type == 'wifi':
                wifi_ssid = data.get('wifi_ssid')
                encryption = data.get('encryption')
                wifi_password = data.get('wifi_password')
                if not (wifi_ssid and encryption and wifi_password):
                    return JsonResponse({'status': 'fail', 'message': 'Complete Wi-Fi details are required'}, status=400)
                wifi_content = f"WIFI:T:{encryption};S:{wifi_ssid};P:{wifi_password};;"
                qr.add_data(wifi_content)
            
            elif qr_type == 'call':
                phone_number = data.get('phone_number')
                if not phone_number:
                    return JsonResponse({'status': 'fail', 'message': 'Phone number is required for type "call"'}, status=400)
                tel_data = f"tel:{phone_number}"
                qr.add_data(tel_data)
            
            else:
                return JsonResponse({'status': 'fail', 'message': 'Invalid type'}, status=400)

            qr.make(fit=True)
            img = qr.make_image(fill_color=fill_color, back_color=background_color).convert('RGB')

            # Process logo if provided
            if logo_file:
                # Since logo_file is provided in JSON, you'd need to handle it differently
                # You can use base64 encoded strings for images in JSON payloads
                # Example of handling base64 encoded image (if logo_file was base64 encoded):
                logo_data = base64.b64decode(logo_file)
                logo = Image.open(BytesIO(logo_data))
                qr_size = min(img.size)
                max_logo_size = qr_size // 5
                logo_size = min(max_logo_size, min(logo.size))
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

                mask = Image.new('L', (logo_size, logo_size), 0)
                draw = ImageDraw.Draw(mask)

                if logo_shape == 'circle':
                    draw.ellipse((0, 0, logo_size, logo_size), fill=255)
                    logo = ImageOps.fit(logo, (logo_size, logo_size), centering=(0.5, 0.5))
                    logo.putalpha(mask)

                elif logo_shape == 'square':
                    if logo_corner == 'rounded':
                        radius = logo_size // 5
                        draw.rounded_rectangle((0, 0, logo_size, logo_size), radius, fill=255)
                    else:
                        draw.rectangle((0, 0, logo_size, logo_size), fill=255)
                    logo.putalpha(mask)

                pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                img.paste(logo, pos, logo)

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

            response_data['qr_code'] = img_str
            response_data['status'] = 'success'
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=405)



#-----------------------------------------------Terms And Conditions--------------------------------------------------#
def terms_and_conditions(request):
    return render(request,'QRcodePro/terms_conditions.html')


#--------------------------------------------------Privacy Policy------------------------------------------------------#
def privacy_policy(request):
    return render(request, 'QRcodePro/privacy_policy.html')