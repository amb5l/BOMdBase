call .venv\Scripts\activate.bat
rundll32 url.dll,FileProtocolHandler http://127.0.0.1:8000/
python manage.py runserver