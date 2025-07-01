#!/bin/bash

VENV_PATH="/home/ubuntu/publicmanager/1gov_saude"

if [ ! -f "$VENV_PATH/bin/activate" ]; then
  echo "O ambiente virtual não foi encontrado em $VENV_PATH"
  exit 1
fi

source "$VENV_PATH/bin/activate"

cd /home/ubuntu/publicmanager || exit

python manage.py migrate

source .env
touch nome_do_script.sh

#Verifica o valor de DEBUG
if [ "$DEBUG" = "True" ]; then
    echo "Iniciando o servidor de desenvolvimento (runserver)..."
    python manage.py collectstatic --noinput

    python manage.py runserver 127.0.0.1:8000
else
   
    while ! nc -z 0.0.0.0 6379; do
      echo "Aguardando Redis..."
      sleep 1
    done

    echo "Iniciando o servico atraves do UVICORN"
    python manage.py collectstatic --noinput
    uvicorn publicmanager.asgi:application --host 127.0.0.1 --port 8000
fi
