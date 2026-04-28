FROM python:3.11

# Instalar dependencias del sistema para ODBC
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    odbc-postgresql \
    && rm -rf /var/lib/apt/lists/*

# Agregar Microsoft repository
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Usar el puerto de variable de entorno o default 5000
EXPOSE 5000
CMD exec gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2
