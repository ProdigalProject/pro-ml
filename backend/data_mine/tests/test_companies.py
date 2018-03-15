from django.test import TestCase
from stocks.models import Company


class CompanyTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        Company.objects.create(
            company_name='Prodigal ML', 
            ticker='PDG-ML', 
            exchange='UIUC Stock Exchange') 

    def test_company_create(self):
        lion = Company.objects.get(ticker="PDG-ML")
        self.assertEqual(lion.company_name, "Prodigal ML")
