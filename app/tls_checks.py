import ssl
import socket
from urllib.parse import urlparse


def check_tls(url):

    hostname = urlparse(url).hostname

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                version = ssock.version()

        return {
            "tls_version": version,
            "issuer": cert.get("issuer")
        }

    except Exception as e:
        return {
            "error": str(e)
        }