import warnings

import typer

warnings.filterwarnings("ignore", category=UserWarning)

from . import vms
from . import data

cli = typer.Typer()
cli.add_typer(data.app, name="data")
cli.add_typer(vms.app, name="vms")

