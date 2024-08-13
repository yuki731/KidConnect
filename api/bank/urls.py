from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSignupView, signin, UserDetailView, ChildrenInFamilyView, ChildPocketMoneyView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', signin, name='signin'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('family/children/', ChildrenInFamilyView.as_view(), name='children_in_family'),
    path('child/<int:child_id>/pocket-money/', ChildPocketMoneyView.as_view(), name='child_pocket_money'),
]
