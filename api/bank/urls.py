from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSignupView, signin, UserDetailView, ChildrenInFamilyView, ChildPocketMoneyView, CreateJobCardView, ApprovalJobRequestView, ApprovalWithdrawalRequestView, ChildDashboardView, TaskView, ReportJobView, CreateWithdrawalRequestView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', signin, name='signin'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('family/children/', ChildrenInFamilyView.as_view(), name='children_in_family'),
    path('child/<int:child_id>/pocket-money/', ChildPocketMoneyView.as_view(), name='child_pocket_money'),
    path('child/<int:child_id>/pocket-money/<int:job_card_id>/', ChildPocketMoneyView.as_view(), name='child_pocket_money_delete'),
    path('create-job-card/', CreateJobCardView.as_view(), name='create_job_card'),
    path('approval-job-request/<int:job_report_id>/', ApprovalJobRequestView.as_view(), name='approval_job_request'),
    path('approval-withdrawal-request/<int:withdrawal_request_id>/', ApprovalWithdrawalRequestView.as_view(), name='approval_withdrawal_request'),
    path('child-dashboard/', ChildDashboardView.as_view(), name='child_dashboard'),
    path('task-view/', TaskView.as_view(), name='task_view'),
    path('report-job/<int:job_id>/', ReportJobView.as_view(), name='report_job'),
    path('create-withdrawal-request/', CreateWithdrawalRequestView.as_view(), name='create_withdrawal_request'),
]
