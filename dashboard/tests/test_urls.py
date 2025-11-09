from django.test import Client
from decimal import Decimal
from dashboard.models.Receita import Receita
from dashboard.models.Ingrediente import Ingrediente


def test_receitas_endpoint():
    """
    Testa o endpoint /api/dashboard/receitas/ usando o banco Atlas real.
    Verifica se a listagem de receitas está funcionando corretamente.
    """
    client = Client()

    # Limpa as coleções antes do teste
    Receita.drop_collection()
    Ingrediente.drop_collection()

    # Cria uma receita de teste
    receita = Receita(
        nome="Bolo de Cenoura",
        categoria="Sobremesa",
        tempo_preparo_horas=0,
        tempo_preparo_minutos=40,
        porcao_individual=Decimal("150.00"),
        medida="g",
        modo_preparo="Misture, bata e asse."
    ).save()

    # Cria um ingrediente relacionado (agora com campo 'alimento')
    Ingrediente(
        receita=receita,
        alimento="Farinha de Trigo",
        peso_bruto=Decimal("120"),
        peso_liquido=Decimal("100")
    ).save()

    # Faz a requisição ao endpoint correto
    response = client.get("/api/dashboard/receitas/")

    # Verifica o status HTTP
    assert response.status_code in (200, 201), f"Status retornado: {response.status_code}"

    data = response.json()

    # Pode ser lista ou dict dependendo da view — validar ambos
    if isinstance(data, list):
        assert len(data) >= 1
        assert data[0]["nome"] == "Bolo de Cenoura"
    elif isinstance(data, dict):
        assert "nome" in data
    else:
        raise AssertionError(f"Formato inesperado: {type(data)}")

    print(" Endpoint de receitas testado com sucesso!")