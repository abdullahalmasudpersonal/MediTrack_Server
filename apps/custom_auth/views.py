from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from apps.users.models import User 
from apps.users.serializers import UserSerializer
from .serializers import UserLimitedSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from apps.core.middleware.customAuthGird import custom_auth_gird
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims
    refresh['email'] = user.email
    refresh['role'] = user.role

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, is_deleted=False, status='active')
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserLimitedSerializer(user)
    tokens = get_tokens_for_user(user)
    return Response({'message': 'Login successful',"user":serializer.data, 'tokens': tokens}, status=status.HTTP_200_OK)

@api_view(['POST'])
@custom_auth_gird(allowed_roles=['admin','doctor','patient'])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({'detail': 'Both old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(old_password, user.password):
     return Response({'detail': 'Old password is incorrect'}, status=400)
    
    if check_password(new_password, user.password):
        return Response({'detail': 'New password cannot be the same as the old password'}, status=400)
        
    user.password = make_password(new_password)
    user.save()

    return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)