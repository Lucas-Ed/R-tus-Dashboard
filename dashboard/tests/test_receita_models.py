from decimal import Decimal
from dashboard.models.Receita import Receita


def test_criar_receita_salvar_e_buscar():
    """
    Testa a criação e persistência de uma receita real no MongoDB Atlas.
    """
    Receita.drop_collection()  # limpa antes do teste

    receita = Receita(
        nome="Bolo de Chocolate",
        categoria="Sobremesa",
        tempo_preparo_horas=0,
        tempo_preparo_minutos=50,
        porcao_individual=Decimal("200.00"),
        medida="g",
        modo_preparo="Misture os ingredientes e asse por 50 minutos."
    )
    receita.save()

    todas = Receita.objects()
    assert todas.count() == 1
    primeira = todas.first()
    assert primeira.nome == "Bolo de Chocolate"
    assert primeira.porcao_individual == Decimal("200.00")