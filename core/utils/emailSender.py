from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
import os
from django.conf import settings


def sendEmail(subject, template_name, context, to_email):
    """
    Sends an email with both plain text and HTML content.

    Args:
        subject (str): The subject of the email.
        template_name (str): Path to the HTML template for the email body.
        context (dict): Context data for rendering the template.
        to_email (str): Recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Render the HTML content
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)  # Plain text version
        from_email = 'Keywordme.io <support@keywordme.io>'
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        image_name = 'keywordme.png'
        image_path = os.path.join(settings.IMAGE_PATH, 'images', image_name )
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', f'<{image_name.split(".")[0]}>')
            email.attach(img)
        email.send()
        return True
    except Exception as e:
        return False
