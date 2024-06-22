from rest_framework_simplejwt.tokens import AccessToken

#adding other user fields to token
class CustomAccessToken(AccessToken):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload['user_id']= user.id
        self.payload['email'] = user.email
        self.payload['role'] = user.role