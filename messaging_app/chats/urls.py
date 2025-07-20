from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

router = routers.NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
