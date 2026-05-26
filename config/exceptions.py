from rest_framework.views import exception_handler
from django.utils import timezone


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code

        if isinstance(response.data, dict) and 'detail' in response.data:
            message = response.data['detail']
        else:
            message = str(response.data)

        error_code = exc.__class__.__name__.upper()

        response.data = {
            "status": status_code,
            "error_code": error_code,
            "message": message,
            "timestamp": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    return response