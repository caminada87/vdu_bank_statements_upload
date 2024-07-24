FROM python:3.11-slim
WORKDIR /app/python-app

COPY . .

RUN pip3 install -r requirements.txt --proxy http://autoproxy.ktag.ch:8080

EXPOSE 5050

CMD gunicorn app:app --bind=0.0.0.0:5050 --forwarded-allow-ips="*" --timeout 0 --workers 4