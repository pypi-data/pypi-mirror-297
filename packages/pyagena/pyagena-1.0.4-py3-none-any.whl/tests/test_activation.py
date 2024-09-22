import unittest;
import pyagena;
import tests.credentials as credentials

class TestActivation(unittest.TestCase):
    def test_activation(self):
        pyagena.local_api_activate_license(credentials.agena_key)
        mode=pyagena.local_api_show_license(asJson=True)['Mode']
        invalid = mode in ['', 'FreeTrial', 'TimedTrial']
        self.assertFalse(invalid)

        pyagena.local_api_activate_license(credentials.agena_key)
        mode=pyagena.local_api_show_license(asJson=True)['Mode']
        invalid = mode in ['', 'FreeTrial', 'TimedTrial']
        self.assertFalse(invalid)

        pyagena.local_api_deactivate_license()
        mode=pyagena.local_api_show_license(asJson=True)['Mode']
        invalid = mode in ['', 'FreeTrial', 'TimedTrial']
        self.assertTrue(invalid)
        
        pyagena.local_api_deactivate_license()
        mode=pyagena.local_api_show_license(asJson=True)['Mode']
        invalid = mode in ['', 'FreeTrial', 'TimedTrial']
        self.assertTrue(invalid)

        pyagena.local_api_activate_license(credentials.agena_key)
        mode=pyagena.local_api_show_license(asJson=True)['Mode']
        invalid = mode in ['', 'FreeTrial', 'TimedTrial']
        self.assertFalse(invalid)

    