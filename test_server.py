from server import app
import unittest2
import json

class FlaskRESTAPITests(unittest2.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 
        
    def test_gene_return_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/gene/abcc13') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        
    def test_gene_content(self):
        result = self.app.get('/gene/abcc13') 

        # parse the return data and assert
        data = json.loads(result.data)
        self.assertEqual(len(data['genes']), 3) # expecting 3 results
        self.assertEqual(data['genes'][0]['id'], 'ENSDARG00000062519')
        self.assertEqual(data['genes'][1]['id'], 'ENSG00000243064')
        self.assertEqual(data['genes'][2]['id'], 'ENSMMUG00000020090')
        
    def test_human_gene_return_code(self):
        result = self.app.get('/gene/brca2/homo_sapiens') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        
    def test_human_gene_content(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/gene/brca2/homo_sapiens') 

        data = json.loads(result.data)
        self.assertEqual(len(data['genes']), 1) # only 1 result should be returned
        self.assertEqual(data['genes'][0]['id'], 'ENSG00000139618')
        self.assertEqual(data['genes'][0]['species'], 'homo_sapiens')
        
