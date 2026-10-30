import socket
import pytest


@pytest.fixture(autouse=True)
def sin_red(monkeypatch):
    def bloquear(*args, **kwargs):
        raise AssertionError("Las pruebas no pueden abrir conexiones de red.")
    monkeypatch.setattr(socket.socket, "connect", bloquear)
    monkeypatch.setattr(socket.socket, "connect_ex", bloquear)
    monkeypatch.setattr(socket, "create_connection", bloquear)
