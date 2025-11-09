from mongoengine import Document, ReferenceField, DecimalField, DateTimeField, StringField
import datetime
from decimal import Decimal


class Ingrediente(Document):
    receita = ReferenceField('Receita', required=True, reverse_delete_rule=2)  # CASCADE
    alimento = StringField(required=True)  
    peso_bruto = DecimalField(precision=2)
    peso_liquido = DecimalField(precision=2)
    peso_processado = DecimalField(precision=2, default=None)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'ingredientes',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return f"{self.alimento} - {self.receita.nome}"

    def clean(self):
        """
        Garante que peso_processado tenha um valor.
        Se não for informado, assume o valor de peso_liquido.
        """
        if self.peso_processado is None:
            self.peso_processado = self.peso_liquido