from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Message  # adjust import based on your project structure

User = get_user_model()


@login_required
def delete_user(request):
    """Deletes the currently logged-in user."""
    user = request.user
    user.delete()  # Triggers the post_delete signal
    return redirect('home')  # Change to your desired landing page


def get_conversation_with_replies(conversation_id):
    """
    Retrieve all top-level messages in a conversation along with all nested replies.
    Uses select_related for sender/receiver and prefetch_related for replies.
    """
    # Fetch only top-level messages in this conversation
    top_level_messages = (
        Message.objects
        .filter(conversation_id=conversation_id, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            'replies__sender',
            'replies__receiver',
            'replies__replies'  # Prefetch second-level replies
        )
    )

    return top_level_messages


def fetch_all_replies(message):
    """
    Recursively fetch all replies to a message (threaded format).
    """
    replies = message.replies.all().select_related('sender', 'receiver')
    for reply in replies:
        reply.all_replies = fetch_all_replies(reply)
    return replies
