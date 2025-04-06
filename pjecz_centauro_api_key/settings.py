"""
Settings

Para que la configuración no sea estática en el código,
se utiliza la librería pydantic para cargar la configuración desde
Google Secret Manager como primera opción, luego de un archivo .env
que se usa en local y por último de variables de entorno.

Para desarrollo debe crear un archivo .env en la raíz del proyecto
con las siguientes variables:

- DB_URL
- ORIGINS
- SALT
- USER_EMAIL
- USER_HASHED_PASSWORD
- USER_API_KEY

Para producción vaya a Google Secret Manager en
https://console.cloud.google.com/security/secret-manager
y cree como secretos las siguientes variables de entorno

- pjecz_centauro_api_key_db_url
- pjecz_centauro_api_key_origins
- pjecz_centauro_api_key_salt
- pjecz_centauro_api_key_user_email
- pjecz_centauro_api_key_user_hashed_password
- pjecz_centauro_api_key_user_api_key

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

    db_url: str = get_secret("db_url")
    origins: str = get_secret("origins", "http://localhost:3000")
    salt: str = get_secret("salt")
    tz: str = "America/Mexico_City"
    user_email: str = get_secret("user_email")
    user_nombres: str = get_secret("user_nombres", "Pruebas")
    user_apellido_paterno: str = get_secret("user_apellido_paterno", "Pruebas")
    user_apellido_materno: str = get_secret("user_apellido_materno", "Pruebas")
    user_username: str = get_secret("user_username", "pruebas")
    user_permissions: str = get_secret("user_permissions", "ORDENES")
    user_hashed_password: str = get_secret("user_hashed_password")
    user_disabled: int = get_secret("user_disabled", "0")
    user_api_key: str = get_secret("user_api_key")
    user_api_key_expiracion: str = get_secret("user_api_key_expiracion", "2035-01-01")

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
