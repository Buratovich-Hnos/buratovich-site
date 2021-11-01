import datetime

from mixer.backend.django import mixer

from django.test import TestCase

from website.models import IncomeQuality, TicketsAnalysis, Deliveries, Sales, SpeciesHarvest, Applied, CtaCte
from website.import_tasks import evalDate, evalDateHour, evalFloat, evalInt, evalText, evalTextUTF8

class UtilFunctionsTest(TestCase):

    def setUp(self):
        self.date_dash_ymd = mixer.faker.date(pattern='%Y-%m-%d')
        self.date_dash_dmy = mixer.faker.date(pattern='%d-%m-%Y')
        self.date_slash_ymd = mixer.faker.date(pattern='%Y/%m/%d')
        self.date_slash_dmy = mixer.faker.date(pattern='%d/%m/%Y')
        self.datehour_dash_ymd = mixer.faker.date(pattern='%Y-%m-%d %I:%M:%S %p')
        self.datehour_dash_dmy = mixer.faker.date(pattern='%d-%m-%Y %I:%M:%S %p')
        self.datehour_slash_ymd = mixer.faker.date(pattern='%Y/%m/%d %I:%M:%S %p')
        self.datehour_slash_dmy = mixer.faker.date(pattern='%d/%m/%Y %I:%M:%S %p')
        self.float_num = '1,0'
        self.int_num = '1'
        self.text = 'test_string'
    
    def test_date_format(self):
        self.assertEqual(evalDate(self.date_dash_ymd), None)
        self.assertEqual(evalDate(self.date_dash_dmy), None)
        self.assertEqual(evalDate(self.date_slash_ymd), None)
        self.assertNotEqual(evalDate(self.date_slash_dmy), None)
        self.assertEqual(isinstance(evalDate(self.date_slash_dmy), str), True)
    
    def test_datehour_format(self):
        self.assertEqual(evalDateHour(self.datehour_dash_ymd), None)
        self.assertEqual(evalDateHour(self.datehour_dash_dmy), None)
        self.assertEqual(evalDateHour(self.datehour_slash_ymd), None)
        self.assertNotEqual(evalDateHour(self.datehour_slash_dmy), None)
        self.assertEqual(isinstance(evalDateHour(self.datehour_slash_dmy), str), True)

    def test_float_format(self):
        num = evalFloat(self.float_num)
        self.assertNotEqual(num, None)
        self.assertEqual(isinstance(num, float), True)
        self.assertEqual(num, 1.0)
        # If ValueError return 0
        self.assertEqual(evalFloat('abc'), 0)
    
    def test_int_format(self):
        num = evalInt(self.int_num)
        self.assertNotEqual(num, None)
        self.assertEqual(isinstance(num, int), True)
        self.assertEqual(num, 1)
        # If ValueError return 0
        self.assertEqual(evalInt('abc'), 0)
    
    def test_text_format(self):
        self.assertEqual(evalText(self.text), self.text)
        self.assertEqual(evalTextUTF8(self.text), self.text)