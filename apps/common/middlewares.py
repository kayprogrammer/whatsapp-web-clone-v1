from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user

        try:
            tzname = user.tz.name if user.tz else None
            timezone.activate(tzname)
        except:
            timezone.deactivate()
        
        response = self.get_response(request)
        return response
        
        