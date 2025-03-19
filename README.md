# pjecz-centauro-api-key

Crear un archivo con las siguientes variables de entorno

```ini
# Base de datos MySQL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=
DB_USER=
DB_PASS=

# FastAPI
ORIGINS=http://localhost:3000
SALT=

# Cuenta para pruebas
USER_EMAIL=pruebas@servidor.gob.mx
USER_NOMBRES=Pruebas
USER_APELLIDO_PATERNO=Pruebas
USER_APELLIDO_MATERNO=Pruebas
USER_USERNAME=pruebas
USER_PERMISSIONS="ORDENES,USUARIOS"
USER_HASHED_PASSWORD=
USER_DISABLED=0
USER_API_KEY=
USER_API_KEY_EXPIRACION=2035-03-18
```

Crear un bash script para cargar el entorno de Python y las variables

```bash
# pjecz-centauro-api-key

if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet Centauro API key
else
    echo "== Centauro API key"
fi
echo

if [ -f .env ]
then
    # export $(grep -v '^#' .env | xargs)
    source .env && export $(sed '/^#/d' .env | cut -d= -f1)
    echo "-- Variables de entorno"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_PORT: ${DB_PORT}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   ORIGINS: ${ORIGINS}"
    echo "   SALT: ${SALT}"
    echo "   USER_EMAIL: ${USER_EMAIL}"
    echo "   USER_NOMBRES: ${USER_NOMBRES}"
    echo "   USER_APELLIDO_PATERNO: ${USER_APELLIDO_PATERNO}"
    echo "   USER_APELLIDO_MATERNO: ${USER_APELLIDO_MATERNO}"
    echo "   USER_USERNAME: ${USER_USERNAME}"
    echo "   USER_PERMISSIONS: ${USER_PERMISSIONS}"
    echo "   USER_HASHED_PASSWORD: ${USER_HASHED_PASSWORD}"
    echo "   USER_DISABLED: ${USER_DISABLED}"
    echo "   USER_API_KEY: ${USER_API_KEY}"
    echo "   USER_API_KEY_EXPIRACION: ${USER_API_KEY_EXPIRACION}"
    echo
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    echo "-- Poetry"
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    echo "   $(poetry --version)"
    echo
    echo "-- FastAPI 127.0.0.1:8000"
    alias arrancar="uvicorn --host=127.0.0.1 --port 8000 --reload pjecz_centauro_api_key.main:app"
    echo "   arrancar"
    echo
fi
```
