# chats/middleware.py

from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        # Deny access if current time is before 6AM or after 9PM
        if now < 6 or now > 21:
            return HttpResponseForbidden("Access is restricted during this time.")
        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if request.method == 'POST' and request.path.startswith('/api/'):  # Adjust path prefix as needed
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Remove old entries
            self.request_counts.setdefault(ip, [])
            self.request_counts[ip] = [ts for ts in self.request_counts[ip] if ts > window_start]

            if len(self.request_counts[ip]) >= 5:
                return JsonResponse({
                    'error': 'Rate limit exceeded. Only 5 messages per minute allowed.'
                }, status=429)

            self.request_counts[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip