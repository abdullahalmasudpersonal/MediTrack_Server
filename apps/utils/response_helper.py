from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

def serialize_error_detail(error):
    """
    ✅ Converts DRF ValidationError or ErrorDetail objects into JSON-serializable form.
    """
    print(error,'error')
    if isinstance(error, dict):
        clean = {}
        for key, value in error.items():
            clean[key] = [str(v) if isinstance(v, ErrorDetail) else v for v in value]
        return clean
    elif isinstance(error, list):
        return [str(v) if isinstance(v, ErrorDetail) else v for v in error]
    elif isinstance(error, ErrorDetail):
        return str(error)
    else:
        return str(error)
    
    
def success_response(message: str, data=None, code=status.HTTP_200_OK):
    """
    ✅ Generic success response
    """
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=code)


def error_response(message: str, error=None, code=status.HTTP_400_BAD_REQUEST):
    """
    ❌ Generic error response
    """
    return Response({
        "success": False,
        "message": message,
        "error": serialize_error_detail(error)
        # "error": str(error) if error else None
    }, status=code)
