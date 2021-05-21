from django.core.mail import send_mail


def send_activation_mail(email, activation_code):
    message = f"""Спасибо за регистрацию на сайте нашего спортивного магазина. 
    Активируйте аккаунт по ссылке: http://127.0.0.1:8000/api/v1/activation/?u={activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'test@myshop.com',
        [email, ]
    )
