FROM python:3.11-slim
WORKDIR /app/python-app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD gunicorn app:app --bind=0.0.0.0:5050 --forwarded-allow-ips="*" --timeout 0 --workers 4