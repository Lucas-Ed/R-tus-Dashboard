from django.test import TestCase, Client
from mongoengine import connect, disconnect
from dashboard.models import Documento, RotuloNutricional
import json

class RotulosCRUDTestCase(TestCase):

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

    def test_create_rotulo(self):
        payload = {
            "nome_receita": "Pão Integral",
            "energia_kcal_100": 250,
            "proteinas_g_100": 10,
            "sodio_mg_100": 400
        }
        response = self.client.post(
            "/api/rotulos/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("result", response.json())
        self.assertEqual(RotuloNutricional.objects.count(), 1)

    def test_read_rotulos_list(self):
        doc = Documento(nome_receita="Teste Receita").save()
        RotuloNutricional(documento=doc, energia_kcal_100=100).save()
        response = self.client.get("/api/rotulos/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    def test_update_rotulo(self):
        doc = Documento(nome_receita="Feijão").save()
        rot = RotuloNutricional(documento=doc, energia_kcal_100=150).save()
        payload = {"energia_kcal_100": 300}
        response = self.client.put(
            f"/api/rotulos/{rot.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        rot.reload()
        self.assertEqual(float(rot.energia_kcal_100), 300.0)

    def test_delete_rotulo(self):
        doc = Documento(nome_receita="Arroz").save()
        rot = RotuloNutricional(documento=doc, energia_kcal_100=90).save()
        response = self.client.delete(f"/api/rotulos/{rot.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RotuloNutricional.objects.count(), 0)