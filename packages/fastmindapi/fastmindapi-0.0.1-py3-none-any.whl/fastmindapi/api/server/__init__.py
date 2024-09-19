from fastapi import FastAPI

app = FastAPI()

from .core import Client  # noqa: F401, E402
