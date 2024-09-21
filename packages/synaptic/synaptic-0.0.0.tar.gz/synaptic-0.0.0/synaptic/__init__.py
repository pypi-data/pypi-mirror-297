from .main import cli
from rich.traceback import install
install()
from rich.pretty import install
install()

__all__ = ['cli']