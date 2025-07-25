import click
import click_spinner

from src.api.api_client import APIClient
from src.api.auth_api import AuthAPI
from src.utils.groups.subcommand_group import SubCommandGroup
from src.utils.helpers.validity_enum import ValidityEnum


class KeyCommands:
    def __init__(self):
        self.client = APIClient()
        self.endpoint = AuthAPI(self.client)

    def create_api_key(self, validity):
        with click_spinner.spinner():
            result = self.endpoint.create_api_key(ValidityEnum[validity])
        if result["success"]:
            click.echo(f"API key created successfully: {result['data']}")
        else:
            click.echo(f"Failed to create API key. {result['message']}")

    def list_api_keys(self):
        with click_spinner.spinner():
            result = self.endpoint.list_api_keys()
        if result["success"]:
            click.echo("API Keys:")
            for key in result["data"]:
                click.echo(
                    f"Token: {key['token']}, Created At: {key['created_at']}, Validity: {key['validity']}"
                )
        else:
            click.echo(f"Failed to retrieve API keys. {result['message']}")

    def delete_api_key(self, token):
        with click_spinner.spinner():
            result = self.endpoint.delete_api_key(token)
        if result["success"]:
            click.echo(f"API key deleted successfully. {result['data']}")
        else:
            click.echo(f"Failed to delete API key. {result['message']}")

    def set_api_key(self, api_key):
        with click_spinner.spinner():
            result = self.endpoint.set_api_key(api_key)
        if result:
            click.echo("API key set successfully.")

    def remove_api_key(self):
        with click_spinner.spinner():
            result = self.endpoint.clear_api_key()
        if result:
            click.echo("API key removed successfully.")
        else:
            click.echo("No API key was set.")


@click.group(cls=SubCommandGroup)
@click.pass_context
def key(ctx):
    """API key management commands."""
    ctx.obj = KeyCommands()


@key.command()
@click.option(
    "--validity",
    type=click.Choice(["ONE_HOUR", "ONE_DAY", "ONE_WEEK", "ONE_MONTH", "ONE_YEAR"]),
    default="ONE_DAY",
    show_default=True,
    prompt="Choose validity period",
)
@click.pass_context
def create(ctx, validity):
    """Create a new API key."""
    ctx.obj.create_api_key(validity)


@key.command()
@click.pass_context
def list(ctx):
    """List all API keys."""
    ctx.obj.list_api_keys()


@key.command()
@click.option("--token", prompt=True)
@click.pass_context
def delete(ctx, token):
    """Delete an API key."""
    ctx.obj.delete_api_key(token)


@key.command()
@click.option("--api-key", prompt=True, hide_input=True)
@click.pass_context
def set(ctx, api_key):
    """Set an API key."""
    ctx.obj.set_api_key(api_key)


@key.command()
@click.pass_context
def unset(ctx):
    """Remove the set API key."""
    ctx.obj.remove_api_key()
