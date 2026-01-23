from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['user_id'] = user.id
		token['role'] = getattr(user, 'role', None)
		token['organisation_id'] = getattr(user, 'organisation_id', None)
		return token
