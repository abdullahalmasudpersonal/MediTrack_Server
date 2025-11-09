from rest_framework.decorators import api_view
from .models import Patient
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer
from apps.core.middleware.customAuthGird import custom_auth_gird
from apps.utils.response_helper import success_response, error_response


# Create your views here.
@api_view(["GET"])
@custom_auth_gird(allowed_roles=["admin"])
def getAllPatient(request):
    try:
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        return success_response(
            message="Get all patient successfully", data=serializer.data, code=200
        )

    except Exception as e:
        return error_response(
            message="Failed to fetch get all patient", error=str(e), code=500
        )


@api_view(["GET"])
@custom_auth_gird(allowed_roles=["admin"])
def getSinglePatient(request, pk):
    try:
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient)
        return success_response(
            message="Get single patient successfully", data=serializer.data, code=200
        )

    except Patient.DoesNotExist:
        return error_response(
            message="Patient not found", error="Invalid patient ID", code=404
        )

    except Exception as e:
        return error_response(
            message="Failed to fetch get all patient", error=str(e), code=500
        )
