from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This triggers the post_delete signal
    return redirect('home')  # Adjust to your landing page