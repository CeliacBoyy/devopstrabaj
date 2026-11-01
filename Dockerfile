# Imagen base liviana de Python (slim = más pequeña y con menos superficie de ataque)
FROM python:3.15-slim

# Evita archivos .pyc y muestra los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Se copia primero requirements.txt para aprovechar la caché de Docker.
# si las dependencias no cambian, no se reinstalan en cada build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Se copia solo el código de la aplicación
COPY app ./app

# Buena práctica de seguridad: no ejecutar como root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Docker consulta /health para saber si el contenedor está sano
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]