import unittest
import json
from main import app 

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_cadastro_cliente(self):
        response = self.app.post('/api/cadastro/cliente', json={
            "cpf": "11223344587",  
            "nome": "Maria da Silva",
            "email": "maria@cliente.com",
            "dataDeNascimento": "1990-04-15T12:00:00.000Z",
            "genero": "Feminino",
            "rendaMensal": 4125.7
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json.loads(response.data))

    def test_cadastro_produto(self):
        response = self.app.post('/api/cadastro/produto', json={
            "nome": "PrevBrasil Medium Term",
            "susep": "15414456790201814",
            "expiracaoDeVenda": "2018-12-31T12:00:00.000Z",
            "valorMinimoAporteInicial": 900.0,
            "valorMinimoAporte": 90.0,
            "idadeDeEntrada": 20,
            "idadeDeSaida": 60,
            "carenciaInicialDeResgate": 60,
            "carenciaEntreResgates": 30
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json.loads(response.data))

    def test_contratacao_plano(self):
        response = self.app.post('/api/contratacao/plano', json={
            "cliente_id": "some-test-client-id",  
            "produto_id": "some-test-product-id",
            "aporte": 2200.00,
            "dataDaContratacao": "2019-07-05T12:00:00.000Z",
            "idadeDeAposentadoria": 62
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json.loads(response.data))

    def test_aporte(self):
        response = self.app.post('/api/aporte', json={
            "idCliente": "some-test-client-id",
            "idPlano": "some-test-plan-id",  
            "valorAporte": 115.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json.loads(response.data))

    def test_resgate(self):
        response = self.app.post('/api/resgate', json={
            "idPlano": "some-test-plan-id",
            "valorResgate": 1300.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
