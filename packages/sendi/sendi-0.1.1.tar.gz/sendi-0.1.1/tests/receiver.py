import asyncio
from typing import Any

from slixmpp import ClientXMPP


class XMPPReceiveMsgBot(ClientXMPP):
    def __init__(self, jid: str, password: str, number_message_to_wait: int, timeout: int) -> None:
        ClientXMPP.__init__(self, jid, password)
        self.timeout = timeout
        self.received_messages: list[Any] = []
        self.number_message_to_wait = number_message_to_wait
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("connection_failed", self.connection_failed)

    async def session_start(self, event: dict) -> None:  # noqa: ARG002
        self.send_presence()
        self.get_roster()

        loop_nb = 0
        while len(self.received_messages) < self.number_message_to_wait:
            if loop_nb > self.timeout:
                break
            await asyncio.sleep(1)
            loop_nb += 1
        self.disconnect()

    def connection_failed(self, event: str) -> None:
        print(f"connection failed: {event}")
        self.disconnect()

    def message(self, msg) -> None:  # noqa: ANN001
        self.received_messages.append(msg)
