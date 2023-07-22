from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import jwt

def generate_certificate(request):
    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name')
        course_name = request.POST.get('course_name')
        completion_date = request.POST.get('completion_date')

        certificate = Certificate(
            recipient_name=recipient_name,
            course_name=course_name,
            completion_date=completion_date,
        )
        certificate.save()

        # After saving the certificate, redirect to the display_certificate view with the new certificate's ID
        return redirect('display_certificate', certificate_id=certificate.certificate_id)

    return render(request, 'generate_certificate.html')

def display_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)

    context = {
        'recipient_name': certificate.recipient_name,
        'course_name': certificate.course_name,
        'certificate_id': certificate.certificate_id,  # Assuming you have a 'score' field in the Certificate model
        'completion_date': certificate.completion_date,
    }

    return render(request, 'display_certificate.html', context)

def generate_certificate_pdf(certificate):
    # Create a new PDF document
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Customize the PDF content here using reportlab drawing commands
    # For example, to draw text:
    c.setFont("Helvetica-Bold", 16)

    # Certificate Header
    c.drawString(220, 750, "Certificate of Completion")

    # Certificate Content
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "This is to certify that")
    c.drawString(100, 680, certificate.recipient_name)
    c.drawString(100, 660, "has successfully completed the certification")
    c.drawString(100, 630, certificate.course_name)
    c.drawString(100, 600, "dated")
    c.drawString(100, 580, certificate.completion_date.strftime("%d %B, %Y"))

    # Certificate ID
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, 100, "Certificate ID:")
    c.drawString(500, 100, str(certificate.certificate_id))

    # Save the PDF content and return the buffer
    c.save()
    buffer.seek(0)
    return buffer

def download_certificate_pdf(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)

    # Generate the PDF for the certificate
    pdf_buffer = generate_certificate_pdf(certificate)

    # Serve the PDF as a download
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'
    return response

def verify_certificate(request, certificate_id):
    if request.method == 'POST':
        # Get the JWT token from the POST request
        jwt_token = request.POST.get('jwt_token')

        try:
            # Verify the JWT token using a secret key
            # Replace 'your_secret_key' with your actual secret key used for JWT encoding
            jwt_data = jwt.decode(jwt_token, 'your_secret_key', algorithms=['HS256'])

            # Check if the certificate_id matches the one in the token
            if jwt_data['certificate_id'] == str(certificate_id):
                # Certificate ID matches, proceed with certificate verification logic here
                certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
                context = {
                    'certificate': certificate,
                    'verification_result': 'Certificate is valid and verified.',
                }
                return render(request, 'verification_result.html', context)
            else:
                # Certificate ID doesn't match, show error message
                context = {
                    'verification_result': 'Certificate ID does not match the token.',
                }
                return render(request, 'verification_result.html', context)

        except jwt.ExpiredSignatureError:
            # Token has expired
            context = {
                'verification_result': 'Token has expired. Please try again.',
            }
            return render(request, 'verification_result.html', context)
        except jwt.InvalidTokenError:
            # Invalid token
            context = {
                'verification_result': 'Invalid token. Please try again.',
            }
            return render(request, 'verification_result.html', context)

    # Render the certificate verification form
    context = {
        'certificate_id': certificate_id,
    }
    return render(request, 'certificate_verification.html', context)