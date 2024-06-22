from django.conf import settings
from rest_framework_simplejwt.utils import datetime_to_epoch, aware_utcnow

def custom_jwt_payload_handler(user):
    """
    Custom JWT payload handler.

    This function controls the custom payload that will be included in the JWT token.
    Adjust it according to your needs to include additional user information.
    """
    return {
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'exp': datetime_to_epoch(aware_utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']),
    }
