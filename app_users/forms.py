from django.contrib.auth.forms import UserCreationForm
from app_users.models import Users


class UserRegistration(UserCreationForm):

    class Meta:
        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
