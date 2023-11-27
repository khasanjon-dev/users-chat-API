from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, CustomTokenRefreshView, CustomTokenObtainPairView, ActivateEmailAPIView, \
    SendEmailLinkAPIView

router = DefaultRouter()
router.register('', UserViewSet, 'user')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('activate/<str:uid>/<str:token>/', ActivateEmailAPIView.as_view(), name='activate'),
    path('activate/send-link/', SendEmailLinkAPIView.as_view(), name='send_link'),
    path('', include(router.urls))
]
