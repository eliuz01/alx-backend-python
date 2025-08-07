from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only allow authenticated users.
    - Only allow participants in the conversation to view/edit/delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        # If the object is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If the object is a Message (has conversation)
        if hasattr(obj, 'conversation'):
            if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
                return user in obj.conversation.participants.all()

        return False