from decimal import Decimal
from dashboard.models.Receita import Receita
from dashboard.models.Ingrediente import Ingrediente


def test_criar_ingrediente_usa_peso_liquido_como_processado():
    """
    Testa se o campo peso_processado é definido automaticamente
    quando não for informado e se o campo 'alimento' é armazenado corretamente.
    """
    Receita.drop_collection()
    Ingrediente.drop_collection()

    receita = Receita(nome="Suco Natural", medida="ml")
    receita.save()

    ing = Ingrediente(
        receita=receita,
        alimento="Polpa de Açaí", 
        peso_bruto=Decimal("100.00"),
        peso_liquido=Decimal("80.00")
    )
    ing.clean()
    ing.save()

    assert ing.peso_processado == Decimal("80.00")
    assert ing.alimento == "Polpa de Açaí"  
    assert Ingrediente.objects.count() == 1