import unittest
import os
from db.tests._create import create_db
from db.api import AuthApi
from db.alchemy import Alchemy


TEST_PATH = os.path.dirname(os.path.abspath(__file__))

# class TestCreateOrganizationAccount(unittest.TestCase):
#     def setUp(self):
#         self.db_path = os.path.join(TEST_PATH, 'tmp.db')
#         self.data = create_db(self.db_path)
#
#     def tearDown(self):
#         os.remove(self.db_path)


class TestAuthApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(TEST_PATH, 'tmp.db')
        cls.data = create_db(cls.db_path)

    def test_check_false(self):
        result = AuthApi.check_organization_exists('nobody@test.ru', 'best_org')
        self.assertEqual(result, False, "В базе обнаружен test@test.ru (best_org)")

    def test_check_true(self):
        org = self.data['orgs'][0]
        result = AuthApi.check_organization_exists(org.email_address, org.name)
        self.assertEqual(result, True, "Существующая организация не обнаружена")

    def test_create_new(self):
        email = 'test@test.ru'
        name = 'best_org'
        password = 'pass'

        result = AuthApi.check_organization_exists(email, name)
        self.assertEqual(result, False, 'Добавляемый организатор уже существует')

        result = AuthApi.create_organization_account(email, name, password)
        self.assertEqual(result, True, 'Невозможно добавить организатора в бд')

        result = AuthApi.check_organization_exists(email, name)
        self.assertEqual(result, True, 'Добавленный организатор должен существовать')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_path)


if __name__ == '__main__':
    # # Creating TestSuite
    # auth_test_suite = unittest.TestSuite()
    # auth_test_suite.addTest(unittest.makeSuite(TestCheckOrganizationExists))
    # auth_test_suite.addTest(unittest.makeSuite(TestCreateOrganizationAccount))
    #
    # # Running TestSuite
    # runner = unittest.TextTestRunner()
    # runner.run(auth_test_suite)
    unittest.main()
