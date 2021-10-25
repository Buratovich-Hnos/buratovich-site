from mixer.backend.django import mixer

from django.test import TestCase

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from website.signals import postSave_User, preSave_User

from django.contrib.auth.models import User 
from .models import UserInfo, IncomeQuality, TicketsAnalysis, Deliveries, Sales

# Model Tests

class UserInfoModelTest(TestCase):

    def setUp(self):
        # Disconnect signals
        pre_save.disconnect(receiver=preSave_User, sender=User, dispatch_uid='website.signals.preSave_User')
        post_save.disconnect(receiver=postSave_User, sender=User, dispatch_uid='website.signals.postSave_User')

        user = User.objects.create_user(username='usertest', email='test@test.com', password='mypassword')
        self.user_info = UserInfo.objects.create(
            user = user,
            algoritmo_code = 1,
            company_name = 'Test Company'
        )
    
    def test_userinfo_str(self):
        self.assertTrue(isinstance(self.user_info, UserInfo))
        self.assertEqual(str(self.user_info), self.user_info.company_name)
        self.assertEqual(str(self.user_info), 'Test Company')


class IncomeQualityModelTest(TestCase):

    def setUp(self):
        self.income_quality = mixer.blend(IncomeQuality, ticket='TK 0001 00090480')
    
    def test_incomequality_str(self):
        self.assertTrue(isinstance(self.income_quality, IncomeQuality))
        self.assertEqual(str(self.income_quality), self.income_quality.ticket)
        self.assertEqual(str(self.income_quality), 'TK 0001 00090480')


class TicketsAnalysisModelTest(TestCase):

    def setUp(self):
        self.ticket_analysis = mixer.blend(TicketsAnalysis, ticket='TK 0001 00090480')
    
    def test_ticketsanalysis_str(self):
        self.assertTrue(isinstance(self.ticket_analysis, TicketsAnalysis))
        self.assertEqual(str(self.ticket_analysis), self.ticket_analysis.ticket)
        self.assertEqual(str(self.ticket_analysis), 'TK 0001 00090480')


class DeliveriesModelTest(TestCase):

    def setUp(self):
        self.ticket = mixer.blend(Deliveries, voucher='TK 0021 00042866')
    
    def test_deliveries_str(self):
        self.assertTrue(isinstance(self.ticket, Deliveries))
        self.assertEqual(str(self.ticket), self.ticket.voucher)
        self.assertEqual(str(self.ticket), 'TK 0021 00042866')


class SalesModelTest(TestCase):

    def setUp(self):
        self.sale = mixer.blend(Sales, voucher='VT 0001 00022925')
    
    def test_deliveries_str(self):
        self.assertTrue(isinstance(self.sale, Sales))
        self.assertEqual(str(self.sale), self.sale.voucher)
        self.assertEqual(str(self.sale), 'VT 0001 00022925')