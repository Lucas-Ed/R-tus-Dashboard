from django.test import TestCase
from mongoengine import connect, disconnect
from dashboard.models import Documento, RotuloNutricional, RotuloFrontal
from decimal import Decimal

class ModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        connect('rotus_test_db', host='mongodb://localhost:27017/rotus_test_db')

    @classmethod
    def tearDownClass(cls):
        disconnect()
        super().tearDownClass()

    def setUp(self):
        Documento.drop_collection()
        RotuloNutricional.drop_collection()
        RotuloFrontal.drop_collection()

    def test_criar_documento(self):
        doc = Documento(nome_receita="Bolo de Cenoura", categoria="doce", tipo_alimento="comida")
        doc.save()
        self.assertIsNotNone(doc.id)
        self.assertEqual(Documento.objects.count(), 1)

    def test_relacionamento_rotulo_nutricional(self):
        doc = Documento(nome_receita="Suco Natural").save()
        rot = RotuloNutricional(documento=doc, energia_kcal_100=Decimal("120.5"))
        rot.save()
        self.assertEqual(rot.documento.nome_receita, "Suco Natural")

    def test_rotulo_frontal_flags(self):
        doc = Documento(nome_receita="Pizza Calabresa").save()
        rotulo_f = RotuloFrontal(
            documento=doc,
            alto_sodio=True,
            valor_sodio=Decimal("1000.00")
        ).save()
        self.assertTrue(rotulo_f.alto_sodio)