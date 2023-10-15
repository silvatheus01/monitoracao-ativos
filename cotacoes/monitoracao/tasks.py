from celery import shared_task
from django.utils import timezone
from django.db.models import Model

from monitoracao.models import Quotation, Monitor
from .api.sheets import Spreadsheet    

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

    msg = f'O preço do ativo "{name}" é de R$ {price}'
    if upper_limit < price:
        msg = msg + ' | Esse é o momento de vender.'
    elif lower_limit > price:
        msg = msg + ' | Esse é o momento de comprar.'

    return msg
