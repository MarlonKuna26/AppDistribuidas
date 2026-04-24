#!/usr/bin/env bash
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar el Driver de Microsoft (Ajustado para Render)
if ! [[ -f /opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.so ]]; then
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
  apt-get update
  ACCEPT_EULA=Y apt-get install -y msodbcsql18
fi