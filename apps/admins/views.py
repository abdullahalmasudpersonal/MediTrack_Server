from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.core.middleware.customAuthGird import custom_auth_gird
from .models import Admin
from apps.admins.serializers import AdminSerializer

# Create your views here.
@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getAllAdmin(request):
     admin = Admin.objects.filter(user__status='active',user__is_deleted=False)
     serializer = AdminSerializer(admin, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getSingleAdmin(request,pk):
     admin = Admin.objects.get(user_id=pk,user__status='active',user__is_deleted=False)
     serializer = AdminSerializer(admin)
     return Response(serializer.data, status=status.HTTP_200_OK)

