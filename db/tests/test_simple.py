import unittest
import os
from db.tests._create import create_db
from db.api import AuthApi
from db.alchemy import Alchemy


TEST_PATH = os.path.dirname(os.path.abspath(__file__))


class TestCheckOrganizationExists(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(TEST_PATH, 'tmp.db')
        self.data = create_db(self.db_path)
        Alchemy.get_instance(self.db_path)

    def test_false(self):
        result = AuthApi.check_organization_exists('test@test.ru', 'best_org')
        self.assertEqual(result, False, "В базе обнаружен test@test.ru (best_org)")

    def test_true(self):
        org = self.data['orgs'][0]
        result = AuthApi.check_organization_exists(org.email_address, org.name)
        self.assertEqual(result, True, "Существующая организация не обнаружена")

    def tearDown(self):
        os.remove(self.db_path)


if __name__ == '__main__':
    unittest.main()
