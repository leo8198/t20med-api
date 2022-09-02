from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import codecs
from config import settings

# Class for email integration using SendGrid API
class EmailAPI():

    # Send an email when the operators is created or to reset passwords
    def send_first_password_email(self,to_email: str,access_token: str):


        # Read the template
        with codecs.open('./services/authentication/templates/template_reset_password.html', 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Complete url
        url = settings.reset_password_endpoint + access_token

        # Replace the placeholders in the html
        template_content = template_content.replace('{complete_url}', url)

        from_email = settings.sendgrid_sender_email

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='Resete a sua senha - T20Med',
            html_content=template_content )
        try:
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            return None
        except Exception as e:
            print("Sendgrid Exception: ",e)
            return None

