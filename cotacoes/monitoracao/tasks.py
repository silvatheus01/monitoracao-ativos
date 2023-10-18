from celery import shared_task
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from monitoracao.models import Quotation, Monitor
from .api.sheets import Spreadsheet    
from django.core.mail import send_mail as send_email_django

from django.conf import settings

from math import isclose

def send_email(msg):
    send_email_django(
        subject="Alerta de preço",
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_TO_EMAIL],
        fail_silently=False,
        html_message=msg
    )

def equals(num1, num2):
    return isclose(num1, num2)

def get_monitor(asset_name):
    return Monitor.objects.get(asset__name=asset_name)

def get_security(row):
    spreadsheet = Spreadsheet()
    return spreadsheet.get_security(row)

def show_alert(upper_limit, lower_limit, price):
    return (upper_limit < price or lower_limit > price) and not (equals(upper_limit, price) or equals(lower_limit, price))
    
def handler_log(monitor, security, asset_name):
    price = security.price
    upper_limit = monitor.upper_limit
    lower_limit = monitor.lower_limit
   
    msg_log = f'O preço do ativo {asset_name} é de R$ {price}'
    email_msg = f'O preço do ativo <b>{asset_name}</b> é de <b>R$ {price}</b>'

    if (show_alert(upper_limit, lower_limit, price)):
        if upper_limit < price:
            alert = '. Esse é o momento de vender.'
        else:
            alert = '. Esse é o momento de comprar.'

        msg_log = msg_log + alert
        email_msg = email_msg + alert
        send_email(email_msg)
        
    return msg_log

@shared_task(bind=True)
def save_quote_monitoring(self, asset_name, row):
    try:
        security = get_security(row)
        monitor = get_monitor(asset_name)
    except ObjectDoesNotExist:
        print('O ativo não está acessível')
        return
    except Exception:
        print('Não foi possível acessar os dados da API.')
        return

    price = security.price
    tradetime = timezone.make_aware(security.tradetime)

    msg_log = handler_log(monitor, security, asset_name)
        
    Quotation.objects.create(
        asset=monitor.asset, 
        price=price, 
        recording_date=timezone.now(), 
        trade_date=tradetime
    )

    return msg_log