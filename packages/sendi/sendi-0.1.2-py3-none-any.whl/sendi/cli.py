import logging
import tomllib
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from pydantic.main import BaseModel

from sendi.common import sendi_logger
from sendi.lib import ConnectionType, SecurityLevel, sendi

app = typer.Typer()


class Config(BaseModel):
    host: str
    port: int = 5222
    password: str
    jid: str
    security_level: SecurityLevel = SecurityLevel.SIMPLE
    connection_type: ConnectionType = ConnectionType.STANDARD
    in_thread: bool = False
    lang: str | None = None
    loglevel: int = logging.ERROR


@app.command()
def send(
    config_name: str,
    targets: list[str],
    message: Optional[str] = None,
    file_path: Optional[Path] = None,
    config_file: Path = Path.home().joinpath(".config/.sendi.toml"),
) -> None:
    try:
        with open(config_file, "rb") as file:
            config_data = tomllib.load(file)
    except FileNotFoundError as exc:
        sendi_logger.error(f"❌ Error: Config file {config_file} not provided")
        raise typer.Exit(2) from exc
    except tomllib.TOMLDecodeError as exc:
        sendi_logger.error(f"❌ Error: Config file {config_file} is not a valid toml file")
        raise typer.Exit(2) from exc

    try:
        config = Config.parse_obj(config_data[config_name])
    except ValidationError as exc:
        sendi_logger.error(exc)
        raise typer.Exit(2) from exc

    logging.basicConfig(level=config.loglevel, format="%(levelname)-8s %(message)s")
    result = sendi(
        host=config.host,
        jid=config.jid,
        message=message,
        password=config.password,
        targets=targets,
        port=config.port,
        security_level=config.security_level,
        in_thread=config.in_thread,
        lang=config.lang,
        file_path=file_path if file_path else None,
    )
    if result:
        sendi_logger.info("💬 message properly send")
    else:
        sendi_logger.error("🚩 failed to send message")
        raise typer.Exit(1)
