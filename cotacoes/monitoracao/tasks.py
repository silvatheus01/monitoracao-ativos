from celery import shared_task
from django.utils import timezone

from django.db.models import Model

from monitoracao.models import Quotation, Monitor
from .api.sheets import Spreadsheet    
from django.core.mail import send_mail as send_email_django

from django.conf import settings

def send_email(msg):
    send_email_django(
        subject="Alerta de preço",
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_TO_EMAIL],
        fail_silently=False,
        html_message=msg
    )

@shared_task(bind=True)
def save_quote_monitoring(self, name, row):
    try:
        spreadsheet = Spreadsheet()
        security = spreadsheet.get_security(row)
    except Exception:
        return 'Não foi possível acessar os dados da API.'
    
    price = security.price
    tradetime = security.tradetime

    try:
        monitor = Monitor.objects.get(asset__name=name)
    except Model.DoesNotExist:
        return 'O ativo não está acessível'
    
    now = timezone.now()
    
    quotation = Quotation(
        asset=monitor.asset, 
        price=price, 
        recording_date=now, 
        trade_date=tradetime
    )
    quotation.save()

    upper_limit = monitor.upper_limit
    lower_limit = monitor.lower_limit

    msg_log = f'O preço do ativo {name} é de R$ {price}'
    msg_email = f'O preço do ativo <b>{name}</b> é de <b>R$ {price}</b>'
    if upper_limit < price:
        alert = '. Esse é o momento de vender.'
        msg_log = msg_log + alert
        msg_email = msg_email + alert
        send_email(msg_email)
    elif lower_limit > price:
        alert = '. Esse é o momento de comprar.'
        msg_log = msg_log + alert
        msg_email = msg_email + alert
        send_email(msg_email)

    return msg_log
