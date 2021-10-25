import mutante_bd
import unittest   
import requests

class Test_Mutante(unittest.TestCase):
    
    def test_mutante_api(self):
        test_data = {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}
        resp = requests.post('http://35.175.141.199:3000/mutante', json=test_data)
        self.assertEqual(resp.status_code, 200)

    def test_no_mutante_api(self):
        test_data = {"dna":["ATGCGA","CAGTGC","TTATTT","AGACGG","GCGTCA","TCACTG"]}
        resp = requests.post('http://35.175.141.199:3000/mutante', json=test_data)
        self.assertEqual(resp.status_code, 403)

    def test_mutante(self):
        data = {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}
        es_mutante, mensaje = mutante_bd.mutante(data)
        self.assertEqual(es_mutante, 1)

    def test_no_mutante(self):
        data = {"dna":["ATGCGA","CAGTGC","TTATTT","AGACGG","GCGTCA","TCACTG"]}
        es_mutante, mensaje = mutante_bd.mutante(data)
        self.assertEqual(es_mutante, 0)

    def test_consulta(self):
        error, verificacion = mutante_bd.consulta()
        self.assertEqual(error, "")

if __name__ == '__main__':
    unittest.main()
