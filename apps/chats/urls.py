from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chats.views.chat import ChatPersonalViewSet

router = DefaultRouter()
router.register('', ChatPersonalViewSet, 'chat_personal')
urlpatterns = [
    path('', include(router.urls))
]
