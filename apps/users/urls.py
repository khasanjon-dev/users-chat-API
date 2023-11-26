from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, CustomTokenRefreshView, CustomTokenObtainPairView
from users.views.activate import ActivateEmail

router = DefaultRouter()
router.register('', UserViewSet, 'user')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('activate/<str:uid>/<str:token>/', ActivateEmail.as_view(), name='activate'),
    path('', include(router.urls))
]
