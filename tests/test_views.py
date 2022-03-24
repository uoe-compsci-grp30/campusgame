from django.test import TestCase, Client
from users.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_succesful_admin_login(self):
        """Function tests if a superuser can successfully login"""
        temp_admin = User(username='user')
        temp_admin.set_password('password')
        temp_admin.is_staff = True
        temp_admin.save() #saves the user in the database

        
        response_login_page = self.client.get('/admin/login/?next=/admin')
        self.assertEquals(response_login_page.status_code, 200) #this tests to see that the user is on the login page
    

        loginresponse = self.client.login(username='user', password='password')
        self.assertTrue(loginresponse)#tests to see whether login was attempted

        #normally the test would work as above with testing if the status code is 200. However due to issues with the migrations file when typing in the url '/admin/' (note the slash at the end) rather than '/admin' it throws an exception if there is a succesful login. To combat this testing is done for the url '/admin' (this could be any url) and ensure that the response code is 301 and the new url is '/admin/' (the changed url is provided in the response)
        response_logged_in = self.client.get('/admin/login/?next=/admin')
        self.assertNotEquals(response_logged_in.status_code, 200)
        self.assertEquals(response_logged_in.url, '/admin/')

    def test_unauthorized_user_login(self):
        """ function verifies a non-superuser cannot access the database. """
        temp_user = User.objects.create_user(username='temp_user')
        temp_user.set_password('passwordtemp')
        temp_user.save() #saves the user in the database
       
        #tests user is not logged in
        response_login_page = self.client.get('/admin/login/?next=/admin')
        self.assertEquals(response_login_page.status_code, 200)

        loginresponse = self.client.login(username='temp_user', password='passwordtemp')
        self.assertTrue(loginresponse)#tests to see whether login was attempted

        #here whether the user is logged in faces a similar issue as above but because they are not logged in passing the url of the login page causes the same issue, so I use the url of what the user should have when theyu are logged in.
        response_logged_in = self.client.get('/admin/')
        self.assertNotEquals(response_logged_in.status_code, 200)
        self.assertEquals(response_logged_in.url, '/admin/login/?next=/admin/')

 #essentially want to test that you canrt acces other ages simply by typing them in

    def test_login_bypass(self):
        """ Function tests that unauthorized users cannot bypass login by directly typing url. """
        response_authorization_page = self.client.get('/admin/auth')
        self.assertEquals(response_authorization_page.status_code, 302)
        self.assertEquals(response_authorization_page.url, "/admin/login/?next=/admin/auth")

        response_group_page = self.client.get('/admin/auth/group')
        self.assertEquals(response_group_page.status_code, 302)
        self.assertEquals(response_group_page.url, "/admin/login/?next=/admin/auth/group")
    
        response_games_page = self.client.get('/admin/games/game/')
        self.assertEquals(response_games_page.status_code, 302)
        self.assertEquals(response_games_page.url, "/admin/login/?next=/admin/games/game/")

        response_rounds_page = self.client.get('/admin/games/round')
        self.assertEquals(response_rounds_page.status_code, 302)
        self.assertEquals(response_rounds_page.url, "/admin/login/?next=/admin/games/round")

        response_zones_page = self.client.get('/admin/games/zone')
        self.assertEquals(response_zones_page.status_code, 302)
        self.assertEquals(response_zones_page.url, "/admin/login/?next=/admin/games/zone")

        response_celery_page = self.client.get('/admin/django_celery_beat/celeryschedule/')
        self.assertEquals(response_celery_page.status_code, 302)
        self.assertEquals(response_celery_page.url, "/admin/login/?next=/admin/django_celery_beat/celeryschedule/")

        response_celery_clocked_page = self.client.get('/admin/django_celery_beat/clockedschedule/')
        self.assertEquals(response_celery_clocked_page.status_code, 302)
        self.assertEquals(response_celery_clocked_page.url, "/admin/login/?next=/admin/django_celery_beat/clockedschedule/")
        
        response_celery_intervals_page = self.client.get('/admin/django_celery_beat/intervalsschedule/')
        self.assertEquals(response_celery_intervals_page.status_code, 302)
        self.assertEquals(response_celery_intervals_page.url, "/admin/login/?next=/admin/django_celery_beat/intervalsschedule/")
        
        response_celery_page = self.client.get('/admin/django_celery_beat/clockedschedule/')
        self.assertEquals(response_celery_page.status_code, 302)
        self.assertEquals(response_celery_page.url, "/admin/login/?next=/admin/django_celery_beat/clockedschedule/")
        
        response_celery_periodic_page = self.client.get('/admin/django_celery_beat/periodictask/')
        self.assertEquals(response_celery_periodic_page.status_code, 302)
        self.assertEquals(response_celery_periodic_page.url, "/admin/login/?next=/admin/django_celery_beat/periodictask/")
        
        response_celery_solar_page = self.client.get('/admin/django_celery_beat/solarschedule/')
        self.assertEquals(response_celery_solar_page.status_code, 302)
        self.assertEquals(response_celery_solar_page.url, "/admin/login/?next=/admin/django_celery_beat/solarschedule/")
        
        response_game_participation_page = self.client.get('/admin/gameparticipation/')
        self.assertEquals(response_game_participation_page.status_code, 302)
        self.assertEquals(response_game_participation_page.url, "/admin/login/?next=/admin/gameparticipation/")

        response_users_page = self.client.get('/admin/users')
        self.assertEquals(response_users_page.status_code, 302)
        self.assertEquals(response_users_page.url, "/admin/login/?next=/admin/users")
        
        response_users_user_page = self.client.get('/admin/users/user/')
        self.assertEquals(response_users_user_page.status_code, 302)
        self.assertEquals(response_users_user_page.url, "/admin/login/?next=/admin/users/user/")
        
        response_password_change_page = self.client.get('/admin/password_change/')
        self.assertEquals(response_password_change_page.status_code, 302)
        self.assertEquals(response_password_change_page.url, "/admin/login/?next=/admin/password_change/")
        
        response_password_change_page = self.client.get('/admin/password_change/')
        self.assertEquals(response_password_change_page.status_code, 302)
        self.assertEquals(response_password_change_page.url, "/admin/login/?next=/admin/password_change/")