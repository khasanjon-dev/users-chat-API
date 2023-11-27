from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase


class CustomTokenObtainPairView(TokenViewBase):
    """
    login ya'ni access va refresh token

    ```
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


class CustomTokenRefreshView(TokenViewBase):
    """
    access token olish from refresh token

    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER
