# from functools import wraps
# from rest_framework.response import Response
# import jwt
# from django.conf import settings
# from rest_framework import status
# from apps.users.models import User

# def custom_auth_gird(allowed_roles=None):
#     if allowed_roles is None:
#         allowed_roles = []
        
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             token = request.headers.get('Authorization')
#             if not token:
#                 return Response({'detail': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
#             try:
#                 decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#                 email = decoded.get('email')
#                 if not email:
#                     return Response({'detail': 'Email not found in token'}, status=status.HTTP_401_UNAUTHORIZED)
#                 user = User.objects.get(email=email)
#                 if allowed_roles and user.role not in allowed_roles:
#                     return Response({'detail': 'You are not authorized to view this data.'}, status=status.HTTP_403_FORBIDDEN)
                
#                 request.user = user
                
#                 return view_func(request, *args, **kwargs)
    
#             except User.DoesNotExist:
#                 return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#             except jwt.ExpiredSignatureError:
#                 return Response({'detail': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
#             except jwt.InvalidTokenError:
#                 return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
#             except Exception as e:
#                 return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
#         return _wrapped_view
#     return decorator

from functools import wraps
from rest_framework.response import Response
import jwt
from django.conf import settings
from rest_framework import status
from apps.users.models import User
from apps.admins.models import Admin
from apps.doctors.models import Doctor
from apps.patients.models import Patient

def custom_auth_gird(allowed_roles=None, optional=False):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                if optional:
                    request.user = None
                    return view_func(request, *args, **kwargs)
                else:
                    return Response({'detail': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                email = decoded.get('email')
                if not email:
                    return Response({'detail': 'Email not found in token'}, status=status.HTTP_401_UNAUTHORIZED)
                
                user = User.objects.get(email=email)
                try:
                    if user.role == 'admin':
                        profile = Admin.objects.get(user=user)
                    elif user.role == 'doctor':
                        profile = Doctor.objects.get(user=user)
                    elif user.role == 'patient':
                        profile = Patient.objects.get(user=user)
                    else:
                        profile = None
                    if profile:
                        user.profile_id = profile.id
                except Exception as e:
                    user.profile_id = None

                if allowed_roles and user.role not in allowed_roles:
                    return Response({'detail': 'You are not authorized to view this data.'}, status=status.HTTP_403_FORBIDDEN)

                request.user = user

                return view_func(request, *args, **kwargs)

            except User.DoesNotExist:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except jwt.ExpiredSignatureError:
                return Response({'detail': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return _wrapped_view
    return decorator
