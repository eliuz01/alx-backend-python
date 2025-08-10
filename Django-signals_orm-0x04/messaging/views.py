from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, Http404
from .models import Message

User = get_user_model()


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')


@login_required
def inbox_unread(request):
    unread_messages = Message.unread.unread_for_user(request.user)  # ✅ Uses custom manager
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


@login_required
@cache_page(60)  # ✅ Cache for 60 seconds
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(
        conversation_id=conversation_id,
        sender=request.user,
        parent_message__isnull=True
    ).only('id', 'sender', 'receiver', 'content', 'timestamp')  # ✅ Uses .only()
    return render(request, 'messaging/conversation.html', {'messages': messages})


@login_required
def send_message(request):   
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        receiver = get_object_or_404(User, pk=receiver_id)
        parent_message = None

        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

        return JsonResponse({"status": "success", "message_id": message.id})

    return JsonResponse({"status": "error", "error": "Invalid request"})


@login_required
def message_thread(request, message_id):
    try:
        message = Message.objects.select_related('sender', 'receiver').get(pk=message_id)
    except Message.DoesNotExist:
        raise Http404("Message not found")

    replies = message.replies.select_related('sender', 'receiver').all()
    return render(request, "messaging/thread.html", {"message": message, "replies": replies})
