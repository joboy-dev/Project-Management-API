from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import BlacklistedToken

class BlacklistTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        
        if header is not None:
            access_token = header.split(' ')[1]
            
            if access_token is None:
                return None

            try:
                blacklisted_token = BlacklistedToken.objects.get(token=access_token)
                if blacklisted_token.is_expired():
                    raise AuthenticationFailed('Token is expired')
                else:
                    raise AuthenticationFailed('Token is blacklisted')
            except BlacklistedToken.DoesNotExist:
                return None
    