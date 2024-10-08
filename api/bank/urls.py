from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSignupView, SigninView, UserDetailView, CreateUserAccountView, ChildrenInFamilyView, ChildPocketMoneyView, CreateJobCardView, ApprovalJobRequestView, ApprovalWithdrawalRequestView, ChildDashboardView, TaskView, ReportJobView, CreateWithdrawalRequestView, DeleteJobCardView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('create-user/', CreateUserAccountView.as_view(), name='create-user'),
    path('family/children/', ChildrenInFamilyView.as_view(), name='children_in_family'),
    path('child/<int:child_id>/pocket-money/', ChildPocketMoneyView.as_view(), name='child_pocket_money'),
    path('child/<int:child_id>/pocket-money/', ChildPocketMoneyView.as_view(), name='child_pocket_money_view'),
    path('create-job-card/', CreateJobCardView.as_view(), name='create_job_card'),
    path('approval-job-request/<int:job_report_id>/', ApprovalJobRequestView.as_view(), name='approval_job_request'),
    path('approval-withdrawal-request/<int:withdrawal_request_id>/', ApprovalWithdrawalRequestView.as_view(), name='approval_withdrawal_request'),
    path('child-dashboard/', ChildDashboardView.as_view(), name='child_dashboard'),
    path('task-view/', TaskView.as_view(), name='task_view'),
    path('report-job/<int:job_id>/', ReportJobView.as_view(), name='report_job'),
    path('create-withdrawal-request/', CreateWithdrawalRequestView.as_view(), name='create_withdrawal_request'),
    path('child/<int:child_id>/job-card/<int:job_card_id>/', DeleteJobCardView.as_view(), name='delete_job_card'),
]
