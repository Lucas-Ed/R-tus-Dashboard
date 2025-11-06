import sys
import os
import django
import random
import decimal

from faker import Faker
from faker_food import FoodProvider
from mongoengine import connect

# Adiciona o diretório raiz do projeto no sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Agora que o sys.path inclui a raiz, podemos importar o models do dashboard
from dashboard.models import Documento, RotuloNutricional, RotuloFrontal

# Configurar Faker e adicionar o FoodProvider
fake = Faker('pt_BR')
fake.add_provider(FoodProvider)

# Configuração MongoDB
MONGO_HOST = "mongodb://localhost:27017"
MONGO_DB = "rotus_db"
MONGO_USER = None
MONGO_PASS = None

connect(
    db=MONGO_DB,
    host=MONGO_HOST,
    username=MONGO_USER,
    password=MONGO_PASS,
    alias="default"
)

# Função para gerar decimal aleatório
def rand_decimal(low, high, ndigits=2):
    val = round(random.uniform(low, high), ndigits)
    return decimal.Decimal(str(val))

# Função principal para popular o banco
def create_fake(n=100):
    print(f"Populando {n} registros...")
    for _ in range(n):
        doc = Documento(
            nome_receita=fake.dish(), 
            categoria=random.choice(['doce', 'salgado']),
            tipo_alimento=random.choice(['comida', 'bebida']),
            tempo_preparo_minutos=random.randint(0, 120),
            modo_preparo=fake.text(max_nb_chars=200),
            informacoes_obrigatorias=fake.sentence()
        )
        doc.save()

        r = RotuloNutricional(
            documento=doc,
            porcao_definida_g_ml=rand_decimal(50, 250, 3),
            fator_densidade=rand_decimal(0.8, 1.2, 4),
            energia_kcal_100=rand_decimal(10, 800),
            proteinas_g_100=rand_decimal(0, 50),
            carboidratos_g_100=rand_decimal(0, 90),
            acucares_totais_g_100=rand_decimal(0, 70),
            acucares_adicionados_g_100=rand_decimal(0, 50),
            gorduras_totais_g_100=rand_decimal(0, 60),
            gorduras_saturadas_g_100=rand_decimal(0, 40),
            gorduras_trans_g_100=rand_decimal(0, 5),
            fibra_alimentar_g_100=rand_decimal(0, 20),
            sodio_mg_100=rand_decimal(0, 2500),
            energia_kcal_porcao=decimal.Decimal('0'),
            proteinas_g_porcao=decimal.Decimal('0'),
        )
        porc = float(r.porcao_definida_g_ml)
        r.energia_kcal_porcao = round(float(r.energia_kcal_100) * porc / 100.0, 2)
        r.proteinas_g_porcao = round(float(r.proteinas_g_100) * porc / 100.0, 2)
        r.save()

        rf = RotuloFrontal(
            documento=doc,
            alto_acucares_adicionados=float(r.acucares_adicionados_g_100) > 22,
            alto_gorduras_saturadas=float(r.gorduras_saturadas_g_100) > 6,
            alto_sodio=float(r.sodio_mg_100) > 600,
            valor_acucares_adicionados=r.acucares_adicionados_g_100,
            valor_gorduras_saturadas=r.gorduras_saturadas_g_100,
            valor_sodio=r.sodio_mg_100,
            observacoes=fake.sentence()
        )
        rf.save()
    print("Concluído.")

if __name__ == "__main__":
    create_fake(100)