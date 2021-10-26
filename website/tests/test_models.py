import datetime

from mixer.backend.django import mixer

from django.test import TestCase

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from website.signals import postSave_User, preSave_User

from django.contrib.auth.models import User 
from website.models import UserInfo
from website.models import IncomeQuality, TicketsAnalysis, Deliveries, Sales, SpeciesHarvest, Applied, CtaCte
from website.models import Currencies, Board, City, Rain, RainDetail, Notifications, ViewedNotifications, AccessLog, Careers

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


class SpeciesHarvestModelTest(TestCase):

    def setUp(self):
        self.speciesharvest = mixer.blend(SpeciesHarvest, species_description='TRIGO COSECHA 21/22')
    
    def test_speciesharvest_str(self):
        self.assertTrue(isinstance(self.speciesharvest, SpeciesHarvest))
        self.assertEqual(str(self.speciesharvest), self.speciesharvest.species_description)
        self.assertEqual(str(self.speciesharvest), 'TRIGO COSECHA 21/22')


class AppliedModelTest(TestCase):

    def setUp(self):
        self.applied = mixer.blend(Applied, voucher='FP 0003 00002519')
    
    def test_applied_str(self):
        self.assertTrue(isinstance(self.applied, Applied))
        self.assertEqual(str(self.applied), self.applied.voucher)
        self.assertEqual(str(self.applied), 'FP 0003 00002519')


class CtaCteModelTest(TestCase):

    def setUp(self):
        self.ctacte = mixer.blend(CtaCte, voucher='OP 0001 00067854')
    
    def test_ctacte_str(self):
        self.assertTrue(isinstance(self.ctacte, CtaCte))
        self.assertEqual(str(self.ctacte), self.ctacte.voucher)
        self.assertEqual(str(self.ctacte), 'OP 0001 00067854')


class CurrenciesModelTest(TestCase):

    def setUp(self):
        self.today = datetime.datetime.today()
        self.currency = mixer.blend(Currencies, date=self.today)
    
    def test_currencies_str(self):
        self.assertTrue(isinstance(self.currency, Currencies))
        self.assertEqual(str(self.currency), self.currency.date.strftime('%m/%d/%Y'))
        self.assertEqual(str(self.currency), self.today.strftime('%m/%d/%Y'))


class BoardModelTest(TestCase):

    def setUp(self):
        self.today = datetime.datetime.today()
        self.board = mixer.blend(Board, date=self.today)
    
    def test_board_str(self):
        self.assertTrue(isinstance(self.board, Board))
        self.assertEqual(str(self.board), self.board.date.strftime('%m/%d/%Y'))
        self.assertEqual(str(self.board), self.today.strftime('%m/%d/%Y'))


class RainModelTest(TestCase):

    def setUp(self):
        self.today = datetime.datetime.today()
        self.city = mixer.blend(City, city=mixer.faker.city())
        self.rain = mixer.blend(Rain, date=self.today)
        self.rain_detail = mixer.blend(RainDetail, rain=self.rain, city=self.city)
    
    def test_city_str(self):
        self.assertTrue(isinstance(self.city, City))
        self.assertEqual(str(self.city), self.city.city)

    def test_rain_str(self):
        self.assertTrue(isinstance(self.rain, Rain))
        self.assertEqual(str(self.rain), self.rain.date.strftime('%m/%d/%Y'))
        self.assertEqual(str(self.rain), self.today.strftime('%m/%d/%Y'))
    
    def test_raindetail_str(self):
        self.assertTrue(isinstance(self.rain_detail, RainDetail))
        self.assertEqual(str(self.rain_detail), self.rain_detail.city.city)
        self.assertEqual(str(self.rain_detail), self.city.city)


class NotificationsModelTest(TestCase):

    def setUp(self):
        # Disconnect signals
        pre_save.disconnect(receiver=preSave_User, sender=User, dispatch_uid='website.signals.preSave_User')
        post_save.disconnect(receiver=postSave_User, sender=User, dispatch_uid='website.signals.postSave_User')

        user = User.objects.create_user(username='usertest', email='test@test.com', password='mypassword')
        user_info = UserInfo.objects.create(
            user = user,
            algoritmo_code = 1,
            company_name = 'Test Company'
        )
        self.notification = mixer.blend(Notifications, title='Notification Test')
        self.viewed_notification = mixer.blend(ViewedNotifications, notification=self.notification, user=user)
    
    def test_notifications_str(self):
        self.assertTrue(isinstance(self.notification, Notifications))
        self.assertEqual(str(self.notification), self.notification.title)
        self.assertEqual(str(self.notification), 'Notification Test')
    
    def test_viewednotifications_str(self):
        self.assertTrue(isinstance(self.viewed_notification, ViewedNotifications))
        self.assertEqual(str(self.viewed_notification), self.viewed_notification.user.userinfo.company_name)
        self.assertEqual(str(self.viewed_notification), 'Test Company')


class AccessLogModelTest(TestCase):

    def setUp(self):
        # Disconnect signals
        pre_save.disconnect(receiver=preSave_User, sender=User, dispatch_uid='website.signals.preSave_User')
        post_save.disconnect(receiver=postSave_User, sender=User, dispatch_uid='website.signals.postSave_User')

        user = User.objects.create_user(username='usertest', email='test@test.com', password='mypassword')
        self.today = datetime.datetime.today()
        self.access_log = mixer.blend(AccessLog, logged=self.today, user=user)
    
    def test_accesslog_str(self):
        self.assertTrue(isinstance(self.access_log, AccessLog))
        self.assertEqual(str(self.access_log), self.access_log.logged.strftime('%m/%d/%Y'))
        self.assertEqual(str(self.access_log), self.today.strftime('%m/%d/%Y'))


class CareersModelTest(TestCase):

    def setUp(self):
        self.career = mixer.blend(Careers, title='Test Career')
    
    def test_career_str(self):
        self.assertTrue(isinstance(self.career, Careers))
        self.assertEqual(str(self.career), self.career.title)
        self.assertEqual(str(self.career), 'Test Career')