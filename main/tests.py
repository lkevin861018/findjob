from django.test import TestCase
from django.core.mail import send_mail

# Create your tests here.
send_mail("confirm mail", "<a href='127.0.0.1:8000/main/complete'>點擊認證</a><br>",
          "kevinliang1018@gmail.com", ['kevinliang1018@gmail.com'])
