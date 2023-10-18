# Monitoramento de cotações

## Executando 
Para executar o projeto, primeiro crie um ambiente virtual e o ative:
```
python -m venv venv
source venv/bin/activate
```
Em seguida, instale as dependências do projeto:
```
pip install -r requirements.txt
```
Agora, entre no diretório do projeto e crie um superusuário:

```
python manage.py createsuperuser
```

Execute a aplicação:
```
python manage.py runserver
```

Com as credenciais criadas, entre em `http://127.0.0.1:8000/admin/` para acessar a interface da aplicação.

### Ativar monitoramento
Para ativar o monitoramento dos ativos, abra um terminal e entre com:
```
celery -A quotations worker --loglevel=info -P gevent --concurrency 1 -E
```
Em seguida, abra outro terminal e execute:
```
celery -A quotations beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Envio de email
Dentro do diretório raiz do projeto, crie um arquivo chamado `.env` e insira as suas informações de envio de email, como no exemplo abaixo:

```
EMAIL_HOST = 'smtp.email.com'
EMAIL_PORT = 123
FROM_EMAIL = 'alice@email.com'
TO_EMAIL = 'bob@email.com'
EMAIL_HOST_USER = 'alice'
EMAIL_HOST_PASSWORD = 'pass'
```
