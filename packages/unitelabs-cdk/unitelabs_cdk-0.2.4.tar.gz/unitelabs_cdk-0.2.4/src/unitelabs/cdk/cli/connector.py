import importlib
import importlib.machinery
import importlib.metadata
import importlib.util
import logging

import click

from unitelabs.cdk import AppFactory, compose_app, utils


@click.group()
def connector() -> None:
    """Base cli"""


@connector.command()
@click.option(
    "--app",
    type=str,
    metavar="IMPORT",
    default=utils.find_factory,
    help="The application factory function to load, in the form 'module:name'.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase the verbosity of to debug.",
)
@utils.coroutine
async def start(app, verbose: int):
    """Application Entrypoint"""
    log_level = logging.DEBUG if verbose > 0 else logging.INFO

    create_app = await load_create_app(app)
    app = await compose_app(create_app, log_level=log_level)

    await app.start()


async def load_create_app(location: str) -> AppFactory:
    """
    Dynamically import the application factory from the given location.

    Args:
      location: Where to find the app factory formatted as "module:name".
    """

    module_name, _, factory_name = location.partition(":")

    module = importlib.import_module(module_name)
    create_app = getattr(module, factory_name)

    return create_app


if __name__ == "__main__":
    connector()
