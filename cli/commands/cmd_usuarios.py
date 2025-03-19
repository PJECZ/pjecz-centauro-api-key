"""
CLI Usuarios
"""

from datetime import datetime, timedelta
import os

import click
from dotenv import load_dotenv

from pjecz_centauro_api_key.dependencies.pwgen import generar_api_key

load_dotenv()
USER_ID = 1
USER_EMAIL = os.getenv("USER_EMAIL")


@click.group()
def cli():
    """Usuarios"""


@click.command()
@click.argument("email", type=str)
@click.option("--dias", default=90, help="Cantidad de días para expirar la API Key")
def nueva_api_key(email, dias):
    """Nueva API Key"""
    api_key = generar_api_key(USER_ID, USER_EMAIL)
    api_key_expiracion = datetime.now() + timedelta(days=dias)
    click.echo(f"Usuario: {USER_EMAIL}")
    click.echo(f"API key: {api_key}")
    click.echo(f"Expira:  {api_key_expiracion.strftime('%Y-%m-%d')}")


cli.add_command(nueva_api_key)
