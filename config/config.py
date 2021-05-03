from pydantic import BaseSettings
import os


class Config(BaseSettings):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
