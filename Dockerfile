FROM python:3.7-slim-stretch
WORKDIR /usr/src/app
EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--timeout=500", "--workers=2", "--bind=0.0.0.0:8000", "app.app:app"]
