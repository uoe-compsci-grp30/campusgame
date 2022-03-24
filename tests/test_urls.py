from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from users.views import UserDetailsView, user_detail_from_jwt

class TestUrls(SimpleTestCase):

    def test_obtain_pair_url_resolves(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url_resolves(self):
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

    def test_token_verify_url_resolves(self):
        url = reverse('token_verify')
        self.assertEquals(resolve(url).func.view_class, TokenVerifyView)

    def test_user_details_verify_url_resolves(self):
        url = reverse('user_details', args=[1])
        self.assertEquals(resolve(url).func.view_class, UserDetailsView)

    def test_user_details_jwt_url_resolves(self):
        url = reverse('user_details_jwt')
        self.assertEquals(resolve(url).func, user_detail_from_jwt)