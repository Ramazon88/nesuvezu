from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from nesu.models import Customuser


class Customusercreate(UserChangeForm):
    class Meta(UserChangeForm):
        model = Customuser
        fields = ("username", "partner", "password")

class Customusercreates(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customuser
        fields = ("username", "partner", "password")