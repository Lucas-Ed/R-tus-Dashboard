import pytest
from core.mongo import connect_db


@pytest.fixture(scope="session", autouse=True)
def connect_to_atlas():
    """
    Conecta ao banco MongoDB Atlas antes de todos os testes.
    Usa a função de conexão real (core/mongo.py).
    """
    connect_db()
    yield
    # O mongoengine mantém o alias 'default' ativo,
    # não é necessário desconectar manualmente.