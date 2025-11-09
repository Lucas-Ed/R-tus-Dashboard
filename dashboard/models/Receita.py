from mongoengine import Document, StringField, ReferenceField, DecimalField, BooleanField, IntField, DateTimeField, EnumField
import datetime
from decimal import Decimal

class Receita(Document):
    MEDIDA_CHOICES = ('g', 'ml')
    nome = StringField(required=True, max_length=255)
    categoria = StringField(max_length=100)
    tempo_preparo_horas = IntField(default=0)
    tempo_preparo_minutos = IntField(default=0)
    porcao_individual = DecimalField(precision=2)
    medida = StringField(choices=MEDIDA_CHOICES)
    modo_preparo = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'receitas',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return self.nome