from django.core.management.base import BaseCommand
from dashboard.models.Receita import Receita
from dashboard.models.Ingrediente import Ingrediente
from decimal import Decimal
import random, datetime

class Command(BaseCommand):
    help = 'Popula o banco com receitas e ingredientes aleatórios'

    def handle(self, *args, **options):
        NOMES_RECEITAS = ["Bolo", "Sopa", "Frango", "Salada"]
        CATEGORIAS = ["Doce", "Salgado"]
        INGREDIENTES_POSSIVEIS = ["Farinha", "Leite", "Ovo", "Açúcar"]

        Receita.objects.delete()
        Ingrediente.objects.delete()

        for i in range(100):
            receita = Receita(
                nome=f"{random.choice(NOMES_RECEITAS)} #{i}",
                categoria=random.choice(CATEGORIAS),
                tempo_preparo_minutos=random.randint(10, 90),
                porcao_individual=Decimal(random.uniform(100, 500)).quantize(Decimal("0.01")),
                medida=random.choice(["g", "ml"]),
                modo_preparo="Misture tudo."
            )
            receita.save()

            for _ in range(random.randint(3, 6)):
                ingr = Ingrediente(
                    receita=receita,
                    alimento=random.choice(INGREDIENTES_POSSIVEIS),
                    peso_bruto=Decimal(random.uniform(50, 500)).quantize(Decimal("0.01")),
                    peso_liquido=Decimal(random.uniform(30, 400)).quantize(Decimal("0.01")),
                )
                ingr.clean()
                ingr.save()

            self.stdout.write(self.style.SUCCESS(f"✔ Receita criada: {receita.nome}"))

        self.stdout.write(self.style.SUCCESS(" Banco populado com 100 receitas!"))