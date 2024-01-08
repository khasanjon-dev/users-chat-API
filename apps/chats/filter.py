from django.db.models import Q
from django_filters import FilterSet, CharFilter

from chats.models import ChatPersonal


class ChatFilter(FilterSet):
    user = CharFilter(method='chat_filter')

    class Meta:
        model = ChatPersonal
        fields = ['user']

    def chat_filter(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(Q(sender=user, receiver=value) | Q(sender=value, receiver=user))
