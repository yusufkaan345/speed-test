FROM python:3.9-slim

WORKDIR /app

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Çevre değişkenleri için varsayılan değerler
ENV SMTP_EMAIL=""
ENV SMTP_PASSWORD=""
ENV RECIPIENT_EMAIL=""

# Dashboard için port aç
EXPOSE 8050

# Gunicorn ile başlat
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "dashboard.start_dashboard:create_app()", "--workers", "4"] 