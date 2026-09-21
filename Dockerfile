FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput || true
CMD ["sh","-c","python manage.py makemigrations store --noinput && python manage.py migrate --noinput && python manage.py seed_demo && gunicorn shop.wsgi:application --bind 0.0.0.0:$PORT"]
