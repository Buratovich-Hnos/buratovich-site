from django.test import TestCase

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from website.signals import postSave_User, preSave_User

from django.contrib.auth.models import User 
from .models import UserInfo

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
        self.assertEqual(str(self.user_info), 'Test Company')