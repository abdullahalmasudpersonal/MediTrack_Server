from functools import wraps
from django.http import JsonResponse
import jwt
from django.conf import settings

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            print("Auth Header:", token)
    
            # try:
            #     decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            #     print("Decoded Token:", decoded_payload)
            # except jwt.ExpiredSignatureError:
            #     print("Token expired")
            # except jwt.DecodeError:
            #     print("Token decode error")
        
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'message': 'Unauthorized'}, status=401)

            if hasattr(user, 'role') and user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'message': 'Forbidden'}, status=403)

        return _wrapped_view
    return decorator

