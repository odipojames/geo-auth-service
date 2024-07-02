from rest_framework_simplejwt.tokens import AccessToken

#adding other user fields to token
class CustomAccessToken(AccessToken):
    def __init__(self, user):
        super().__init__()
        self.payload['user_id'] = str(user.id)
        self.payload['email'] = user.email
        self.payload['first_name'] = user.first_name
        self.payload['last_name'] = user.last_name
        self.payload['role'] = user.role
