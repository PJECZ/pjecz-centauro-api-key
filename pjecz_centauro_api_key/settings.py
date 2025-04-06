"""
Settings

Para que la configuración no sea estática en el código,
se utiliza la librería pydantic para cargar la configuración desde
Google Secret Manager como primera opción, luego de un archivo .env
que se usa en local y por último de variables de entorno.

Para desarrollo debe crear un archivo .env en la raíz del proyecto
con las siguientes variables:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_PASS
- DB_USER
- ORIGINS
- SALT
- USER_EMAIL
- USER_NOMBRES
- USER_APELLIDO_PATERNO
- USER_APELLIDO_MATERNO
- USER_USERNAME
- USER_PERMISSIONS
- USER_HASHED_PASSWORD
- USER_DISABLED
- USER_API_KEY
- USER_API_KEY_EXPIRACION

Para producción vaya a Google Secret Manager en
https://console.cloud.google.com/security/secret-manager
y cree como secretos las siguientes variables de entorno

- pjecz_centauro_api_key_db_host
- pjecz_centauro_api_key_db_port
- pjecz_centauro_api_key_db_name
- pjecz_centauro_api_key_db_pass
- pjecz_centauro_api_key_db_user
- pjecz_centauro_api_key_origins
- pjecz_centauro_api_key_salt
- pjecz_centauro_api_key_user_email
- pjecz_centauro_api_key_user_nombres
- pjecz_centauro_api_key_user_apellido_paterno
- pjecz_centauro_api_key_user_apellido_materno
- pjecz_centauro_api_key_user_username
- pjecz_centauro_api_key_user_permissions
- pjecz_centauro_api_key_user_hashed_password
- pjecz_centauro_api_key_user_disabled
- pjecz_centauro_api_key_user_api_key
- pjecz_centauro_api_key_user_api_key_expiracion

E incluya las siguientes variables de entorno

- SERVICE_PREFIX: pjecz_centauro_api_key
"""

import os
from functools import lru_cache

import google.auth
import google.cloud.secretmanager
from pydantic_settings import BaseSettings

SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_centauro_api_key")


def get_secret(secret_id: str, default: str = "") -> str:
    """Get secret from google cloud secret manager"""

    # Si secret_id esta definido como variable de entorno, entonces se usa
    # if secret_id.upper() in os.environ:
    #     return os.environ[secret_id.upper()]

    # Obtener el project id con la libreria de google
    _, project_id = google.auth.default()
    if project_id:
        try:
            # Create the secret manager client
            client = google.cloud.secretmanager.SecretManagerServiceClient()
            # Build the resource name of the secret version
            secret = f"{SERVICE_PREFIX}_{secret_id}"
            name = client.secret_version_path(project_id, secret, "latest")
            # Access the secret version
            response = client.access_secret_version(name=name)
            # Return the decoded payload
            return response.payload.data.decode("UTF-8")
        except Exception:
            pass

    # Si no se encuentra el secreto, entonces se entrega el valor por defecto
    return default


class Settings(BaseSettings):
    """Settings"""

    db_host: str = get_secret("db_host")
    db_port: int = get_secret("db_port", "3306")
    db_name: str = get_secret("db_name")
    db_pass: str = get_secret("db_pass")
    db_user: str = get_secret("db_user")
    origins: str = get_secret("origins")
    salt: str = get_secret("salt")
    tz: str = "America/Mexico_City"
    user_email: str = get_secret("user_email")
    user_nombres: str = get_secret("user_nombres")
    user_apellido_paterno: str = get_secret("user_apellido_paterno")
    user_apellido_materno: str = get_secret("user_apellido_materno")
    user_username: str = get_secret("user_username")
    user_permissions: str = get_secret("user_permissions")
    user_hashed_password: str = get_secret("user_hashed_password")
    user_disabled: int = get_secret("user_disabled", "0")
    user_api_key: str = get_secret("user_api_key")
    user_api_key_expiracion: str = get_secret("user_api_key_expiracion")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
