@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python manage.py makemigrations blackline
python manage.py migrate
python manage.py cargar_productos
python manage.py cargar_resenas
echo.
echo Servidor listo: abre http://127.0.0.1:8000/  (para apagarlo: Ctrl + C)
python manage.py runserver
pause
