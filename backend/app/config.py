import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    model: str


def get_settings() -> Settings:
    """Load settings from the environment."""
    return Settings(
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
        model=os.environ["MODUS_MODEL"],
    )
