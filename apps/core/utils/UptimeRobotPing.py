# views.py (যেখানে তোমার API views আছে)
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ping(request):
    return Response({"UptimeRobot active / Server Active / Database active": "ok"})
