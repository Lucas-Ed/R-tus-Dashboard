from mongoengine import Document, EmbeddedDocument, fields

import datetime
 
class Documento(Document):

    nome_receita = fields.StringField(required=True)

    categoria = fields.StringField(choices=['doce', 'salgado'], default='doce')

    tipo_alimento = fields.StringField(choices=['comida', 'bebida'], default='comida')

    tempo_preparo_minutos = fields.IntField(default=0)

    modo_preparo = fields.StringField()

    informacoes_obrigatorias = fields.StringField()

    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'documento'}
 
class RotuloNutricional(Document):

    documento = fields.ReferenceField(Documento, required=True)

    porcao_definida_g_ml = fields.DecimalField(precision=3, default=0)

    fator_densidade = fields.DecimalField(precision=4, default=1)

    energia_kcal_100 = fields.DecimalField(precision=2)

    proteinas_g_100 = fields.DecimalField(precision=2)

    carboidratos_g_100 = fields.DecimalField(precision=2)

    acucares_totais_g_100 = fields.DecimalField(precision=2)

    acucares_adicionados_g_100 = fields.DecimalField(precision=2)

    gorduras_totais_g_100 = fields.DecimalField(precision=2)

    gorduras_saturadas_g_100 = fields.DecimalField(precision=2)

    gorduras_trans_g_100 = fields.DecimalField(precision=2)

    fibra_alimentar_g_100 = fields.DecimalField(precision=2)

    sodio_mg_100 = fields.DecimalField(precision=2)

    # valores por porção (calculados ou armazenados)

    energia_kcal_porcao = fields.DecimalField(precision=2)

    proteinas_g_porcao = fields.DecimalField(precision=2)

    carboidratos_g_porcao = fields.DecimalField(precision=2)

    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'rotulo_nutricional'}
 
class RotuloFrontal(Document):

    documento = fields.ReferenceField(Documento, required=True)

    alto_acucares_adicionados = fields.BooleanField(default=False)

    alto_gorduras_saturadas = fields.BooleanField(default=False)

    alto_sodio = fields.BooleanField(default=False)

    valor_acucares_adicionados = fields.DecimalField(precision=2, default=0)

    valor_gorduras_saturadas = fields.DecimalField(precision=2, default=0)

    valor_sodio = fields.DecimalField(precision=2, default=0)

    observacoes = fields.StringField()

    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'rotulo_frontal'}
 
# Model de Cliente

class Cliente(Document):
    id_cliente = fields.SequenceField(primary_key=True)
    nome = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'cliente'}



# Model de Ingrediente

class Ingrediente(Document):
    id_ingrediente = fields.SequenceField(primary_key=True)
    nome_ingrediente = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'ingrediente'}