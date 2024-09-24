import contextlib
import ssl
from pathlib import Path

import certifi
import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqTimeout
from slixmpp.features.feature_mechanisms import Failure
from slixmpp.jid import JID
from slixmpp.plugins.xep_0363.http_upload import FileTooBig, HTTPError, UploadServiceNotFound
from slixmpp.stanza import Message, StreamError

from sendi.common import SecurityLevel, sendi_logger

# based on :
# - https://codeberg.org/nicoco/slixmpp/src/branch/pyproject/examples/http_upload.py : MIT
# - https://github.com/Syndace/slixmpp-omemo/blob/main/examples/echo_client.py : AGPL-V3
# - https://github.com/caronc/apprise/tree/v0.9.9/apprise/plugins/NotifyXMPP : MIT


class XMPPSendMsgBot(ClientXMPP):
    def __init__(
        self,
        jid: str,
        password: str,
        host: str = "localhost",
        port: int = 5222,
        security_level: SecurityLevel = SecurityLevel.SIMPLE,
        message_body: str | None = None,
        file_path: Path | None = None,
        targets: list[str] | None = None,
        lang: str | None = None,
    ) -> None:
        """
        Initialize our SliXmppAdapter object
        """
        self.success = False
        self.host = host
        self.port = port
        self.security_level = security_level
        self.secure = security_level in [SecurityLevel.SIMPLE, SecurityLevel.ENCRYPTED]
        self.verify_certificates = self.secure
        self._jid = jid
        self._password = password or ""
        self.file_path = file_path
        self.body = message_body
        self.targets: list[JID] = [JID(target) for target in targets] if targets else []
        self.xep = [
            # xep_0030: Service Discovery
            30,
            # Service Discovery Extensions
            128,
            # xep_0199: XMPP Ping
            199,
            # http upload
            363,
            # OMEMO Media sharing
            454,
            # xhtml-im: needed for http upload
            71,
            # Out of Band Data: needed for http upload
            66,
            # Explicit Message Encryption
            380,
        ]

        slixmpp.ClientXMPP.__init__(self, self._jid, self._password, lang=lang)
        for xep in self.xep:
            # Load xep entries
            self.register_plugin(f"xep_{xep:04d}")

        # Omemo
        from slixmpp.plugins import register_plugin

        from sendi.omemo import XEP_0384Impl

        XEP_0384Impl.STORAGE_PATH = Path.home().joinpath(".cache/sendi_omemo.json")
        register_plugin(XEP_0384Impl)
        self.register_plugin(
            "xep_0384",  # OMEMO Encryption
            module=XEP_0384Impl,
        )

        if self.secure:
            # Don't even try to use the outdated ssl.PROTOCOL_SSLx
            self.ssl_version = ssl.PROTOCOL_TLSv1

            # If the python version supports it, use highest TLS version
            # automatically
            if hasattr(ssl, "PROTOCOL_TLS"):
                # Use the best version of TLS available to us
                self.ssl_version = ssl.PROTOCOL_TLS
            self.ca_certs = None
            if self.verify_certificates:
                # Set the ca_certs variable for certificate verification
                self.ca_certs = self.get_ca_certificates_locations()
                if self.ca_certs is None:
                    sendi_logger.warn(
                        "XMPP Secure comunication can not be verified; "
                        "no local CA certificate file"
                    )

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("connection_failed", self.connection_failed)
        self.add_event_handler("failed_all_auth", self.failed_auth)
        self.add_event_handler("stream_error", self.stream_error)

    @staticmethod
    def get_ca_certificates_locations() -> list[Path]:
        """
        Return possible locations to root certificate authority (CA) bundles.

        Taken from https://golang.org/src/crypto/x509/root_linux.go
        TODO: Maybe refactor to a general utility function?
        """
        candidates = [
            # Debian/Ubuntu/Gentoo etc.
            "/etc/ssl/certs/ca-certificates.crt",
            # Fedora/RHEL 6
            "/etc/pki/tls/certs/ca-bundle.crt",
            # OpenSUSE
            "/etc/ssl/ca-bundle.pem",
            # OpenELEC
            "/etc/pki/tls/cacert.pem",
            # CentOS/RHEL 7
            "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",
            # macOS Homebrew; brew install ca-certificates
            "/usr/local/etc/ca-certificates/cert.pem",
        ]
        # Certifi provides Mozilla's carefully curated collection of Root
        # Certificates for validating the trustworthiness of SSL certificates
        # while verifying the identity of TLS hosts. It has been extracted from
        # the Requests project.
        with contextlib.suppress(ImportError):
            candidates.append(certifi.where())

        path_certificates = []
        for candidate in candidates:
            path = Path(candidate)
            if path.is_file():
                path_certificates.append(path)
        return path_certificates

    def connection_failed(self, event: str) -> None:
        sendi_logger.error(f"connection failed: {event}")
        self.disconnect()

    def failed_auth(self, event: Failure) -> None:
        """After all auth test. Slixmpp test multiple auth before finding a working one"""
        sendi_logger.error(f"bad auth: {event['text']}")

    def stream_error(self, event: StreamError) -> None:
        """Stream error case, can occur with policy-violation error from ejabberd-fail2ban module"""
        sendi_logger.error(f"stream error: {event['text']}")

    async def upload(self, filename: Path) -> str | None:
        try:
            match self.security_level:
                case SecurityLevel.ENCRYPTED:
                    upload_file = self["xep_0454"].upload_file
                case _:
                    upload_file = self["xep_0363"].upload_file
            sendi_logger.debug("upload file")
            url = await upload_file(
                filename,
                domain=self.host,
            )
            sendi_logger.debug("file uploaded")
        except UploadServiceNotFound as exc:
            sendi_logger.error(f"Err: UploadServiceNotFound : {exc}")
            return None
        except (FileTooBig, HTTPError) as exc:
            sendi_logger.error(f"Err: {exc}")
            return None
        except IqTimeout:
            sendi_logger.error("Err: Could not send file in time")
            return None
        except Exception as exc:
            sendi_logger.error(f"Err: {exc}")
            return None
        return url

    def create_http_upload_link(self, url: str, target: JID) -> Message:
        message_html = f'<a href="{url}">{url}</a>'
        message = self.make_message(mto=target, mbody=url, mhtml=message_html)
        message["oob"]["url"] = url
        return message

    async def encrypt_message(self, message: Message, target: JID) -> list[Message]:
        encrypted_messages_data, encryption_errors = await self["xep_0384"].encrypt_message(
            message, target
        )
        if len(encryption_errors) > 0:
            sendi_logger.warn(
                f"There were non-critical errors during encryption: {encryption_errors}"
            )
        encrypted_messages = []
        for namespace, msg in encrypted_messages_data.items():
            msg["eme"]["namespace"] = namespace
            msg["eme"]["name"] = self["xep_0380"].mechanisms[namespace]
            encrypted_messages.append(msg)
        return encrypted_messages

    async def session_start(self, event: dict) -> None:  # noqa: ARG002, C901
        sendi_logger.debug("session start")
        self.send_presence()
        sendi_logger.debug("presence sended")
        self.get_roster()
        sendi_logger.debug("roster obtained")

        targets = list(self.targets)
        if not targets:
            # We always default to notifying ourselves
            targets.append(JID(self.jid))
        # HTTP _UPLOAD
        sendi_logger.debug("upload file")
        url = None
        if self.file_path:
            url = await self.upload(filename=self.file_path)
            if not url:
                sendi_logger.error("no url, disconnect")
                self.disconnect()
                return None
        sendi_logger.debug("uploaded file")
        sendi_logger.debug("prepare message")
        # MESSAGES
        messages_to_send: list[Message] = []
        while len(targets) > 0:
            # Get next target (via JID)
            target = targets.pop(0)
            # HTTP UPLOAD MESSAGE
            if url:
                message = self.create_http_upload_link(url, target)
                if self.security_level == SecurityLevel.ENCRYPTED:
                    messages_to_send.extend(await self.encrypt_message(message, target))
                else:
                    messages_to_send.append(message)
            # Standard Message
            if self.body:
                # The message we wish to send, and the JID that will receive it.
                message = self.make_message(mto=target, mbody=self.body, mtype="chat")
                if self.security_level == SecurityLevel.ENCRYPTED:
                    messages_to_send.extend(await self.encrypt_message(message, target))
                else:
                    messages_to_send.append(message)
        sendi_logger.debug("message to send")
        for message in messages_to_send:
            message.send()
        sendi_logger.debug("disconnect")
        self.disconnect()
        self.success = True
