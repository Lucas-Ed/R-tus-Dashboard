from django.test import TestCase, Client
from mongoengine import connect, disconnect
from dashboard.models import Documento, RotuloNutricional
from decimal import Decimal

class IndicadoresAPITestCase(TestCase):
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
        self.client = Client()

    def test_indicadores_endpoint(self):
        doc1 = Documento(nome_receita="Açaí").save()
        doc2 = Documento(nome_receita="Suco de Laranja").save()
        RotuloNutricional(documento=doc1, energia_kcal_100=Decimal("300.5")).save()
        RotuloNutricional(documento=doc2, energia_kcal_100=Decimal("100.0")).save()
        response = self.client.get("/api/indicadores/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_rotulos", data)
        self.assertEqual(data["total_rotulos"], 2)
        self.assertTrue("avg_energy_kcal_100" in data)
