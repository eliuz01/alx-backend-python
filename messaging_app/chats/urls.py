from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


_ = NestedDefaultRouter(router, r'conversations', lookup='conversation')

urlpatterns = [
    path('', include(router.urls)),
]
