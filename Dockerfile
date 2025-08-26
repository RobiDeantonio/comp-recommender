# Usamos imagen oficial de Python 3.10
FROM python:3.10-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements y luego instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto que usará la app en Render
EXPOSE 10000

# Comando para correr FastAPI con Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "10000"]
