import datetime
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                now = timezone.now()
                last_activity_time = datetime.datetime.fromisoformat(last_activity)
                inactivity_duration = (now - last_activity_time).total_seconds()
                if inactivity_duration > settings.SESSION_COOKIE_AGE:
                    logout(request)  # Cierra la sesión si el tiempo de inactividad supera el límite
            request.session['last_activity'] = timezone.now().isoformat()
        response = self.get_response(request)
        return response