import asyncio
import os
import tomllib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sendi.cli import Config, app
from sendi.lib import sendi
from tests.receiver import XMPPReceiveMsgBot

runner = CliRunner()


@pytest.fixture
def config_file() -> str:
    return os.environ.get("TEST_CONFIG_FILE", default="test.toml")


@pytest.fixture
def config_data(config_file: str) -> dict:
    with open(config_file, "rb") as file:
        return tomllib.load(file)


@pytest.fixture
def receiver1_config(config_data: dict) -> dict:
    return config_data["receiver1"]


@pytest.fixture
def receiver2_config(config_data: dict) -> dict:
    return config_data["receiver2"]


@pytest.fixture
def sender_config(config_data: dict) -> Config:
    return Config.parse_obj(config_data["sender"])


def test_app() -> None:
    result = runner.invoke(
        app,
        [],
    )
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Usage" in result.stdout


def test_verify_empty(receiver1_config: dict, receiver2_config: dict) -> None:
    with asyncio.Runner() as asyncrunner:
        xmpp_bot = XMPPReceiveMsgBot(
            jid=receiver1_config["jid"],
            password=receiver1_config["password"],
            number_message_to_wait=0,
            timeout=10,
        )
        xmpp_bot_2 = XMPPReceiveMsgBot(
            jid=receiver2_config["jid"],
            password=receiver2_config["password"],
            number_message_to_wait=0,
            timeout=10,
        )
        xmpp_bot.connect(force_starttls=True)
        xmpp_bot_2.connect(force_starttls=True)
        asyncrunner.get_loop().run_until_complete(xmpp_bot.disconnected)

    assert len(xmpp_bot_2.received_messages) == len(xmpp_bot.received_messages)
    assert len(xmpp_bot.received_messages) == 0


def test_send(receiver1_config: dict, receiver2_config: dict, sender_config: Config) -> None:
    message = "Test"
    file_path = Path("tests/test_image.jpg")
    assert file_path.is_file()
    targets = [receiver2_config["jid"], receiver1_config["jid"]]
    result = sendi(
        host=sender_config.host,
        jid=sender_config.jid,
        message=message,
        password=sender_config.password,
        targets=targets,
        port=sender_config.port,
        security_level=sender_config.security_level,
        in_thread=sender_config.in_thread,
        lang=sender_config.lang,
        file_path=file_path if file_path else None,
    )
    assert result


def test_receive(receiver1_config: dict, receiver2_config: dict) -> None:
    with asyncio.Runner() as asyncrunner:
        xmpp_bot = XMPPReceiveMsgBot(
            jid=receiver1_config["jid"],
            password=receiver1_config["password"],
            number_message_to_wait=2,
            timeout=300,
        )
        xmpp_bot_2 = XMPPReceiveMsgBot(
            jid=receiver2_config["jid"],
            password=receiver2_config["password"],
            number_message_to_wait=2,
            timeout=300,
        )
        xmpp_bot.connect(force_starttls=True)
        xmpp_bot_2.connect(force_starttls=True)
        asyncrunner.get_loop().run_until_complete(xmpp_bot.disconnected)

    assert len(xmpp_bot_2.received_messages) == len(xmpp_bot.received_messages)
    assert len(xmpp_bot.received_messages) == 2  # noqa: PLR2004
    if "Test" in str(xmpp_bot.received_messages[0]):
        simple_message = xmpp_bot.received_messages[0]
        file_message = xmpp_bot.received_messages[1]
    else:
        simple_message = xmpp_bot.received_messages[1]
        file_message = xmpp_bot.received_messages[0]
    assert "Test" in str(simple_message)
    assert "test_image.jpg" in str(file_message)
