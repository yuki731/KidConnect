from django.urls import path
from .views import UserSignupView, signin

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', signin, name='signin'),
]
