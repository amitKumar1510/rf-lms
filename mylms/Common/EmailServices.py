from rest_framework.response import Response
from authApp.models import CustomUser
from django.core.mail import EmailMessage

class MailService():
    def send_Credentials(email,password):
        try:
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'error': 'Email not found. Please provide a correct email.'}, status=404)

            subject = "Thank You for Registering"
            email_from = "amtcuo8579@gmail.com"
            email_to = [email]
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px; color: #333;">
                <div style="max-width: 600px; margin: auto; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                <h2 style="color: #2c3e50; text-align: center;">🎉 Welcome to SikshaAI!</h2>

                <p style="font-size: 16px;">Hi <strong>{user.first_name or 'User'}</strong>,</p>

                <p style="font-size: 16px;">
                    We're excited to have you join us! Your role has been registered as: <strong style="color: #007BFF;">{user.role}</strong>
                </p>

                <p style="font-size: 16px;">Here are your login details:</p>
                <ul style="font-size: 16px; line-height: 1.6;">
                    <li><strong>Email:</strong> {user.email}</li>
                    <li><strong>Temporary Password:</strong> {password}</li>
                </ul>

                <p style="font-size: 15px; color: #e67e22;"><strong>Important:</strong> This is a temporary password provided for initial login. Please update your password immediately after logging in.</p>

                <p style="font-size: 14px; color: #999;">
                    ⚠️ This email was generated for testing purposes by the development team. If you did not request or expect this account, please contact <a href="mailto:support@sikshaai.com">support@sikshaai.com</a> immediately.
                </p>

                <br>
                <p style="font-size: 16px;">Best regards,<br><strong>The SikshaAI Team</strong></p>

                <hr style="margin-top: 30px;">
                <p style="font-size: 12px; color: #bbb; text-align: center;">
                    © 2025 SikshaAI. All rights reserved.
                </p>
                </div>
            </body>
            </html>
            """


            message = EmailMessage(subject, html_message, email_from, email_to)
            message.content_subtype = "html"
            message.send()

            return Response({'message': 'Registration email sent successfully'}, status=200)

        except Exception as e:
            return Response({'error': f'Error in sending email: {str(e)}'}, status=500)
        

    def send_Mail(self, email, subject,  html_message):
        try:
            email_from = "amtcuo8579@gmail.com"
            email_to = [email]

            message = EmailMessage(subject, html_message, email_from, email_to)
            message.content_subtype = "html"
            message.send()

            return Response({'message': 'email sent successfully'}, status=200)

        except Exception as e:
            return Response({'error': f'Error in sending email: {str(e)}'}, status=500)
