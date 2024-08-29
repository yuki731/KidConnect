from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Sum, Case, When, F, DecimalField, IntegerField


from .models import PocketMoney, JobCard, JobReport, WithdrawalRequest
from .serializers import UserSignupSerializer, LoginSerializer, CreateUserSerializer, UserSerializer, PocketMoneySerializer, JobCardSerializer, JobReportSerializer, WithdrawalRequestSerializer

User = get_user_model()

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}") 
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            # ユーザーを作成
            user = serializer.save()

            # 新しいグループを作成（必要に応じて）
            group, created = Group.objects.get_or_create(name='Parents')  # グループ名を適切に設定

            unique_group_name = f"{user.family_name}_{user.id}"
            family_group, created = Group.objects.get_or_create(name=unique_group_name)

            # ユーザーをグループに追加
            user.groups.add(group)
            user.groups.add(family_group)

            # 成功メッセージを返す
            return Response({"message": "User created and added to group successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(f"Authenticating user: {username}")  # ユーザー名をログに出力
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                print("Authentication failed")  # 認証失敗をログに出力
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)  # エラーメッセージをログに出力
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############# Parents Views ##############

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Parents').exists():
            return Response({"detail": "You do not have permission to create user accounts."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()

            # 現在ログインしている親ユーザーを取得
            parent_user = request.user
            family_name = parent_user.family_name  # 親ユーザーからファミリーネーム（family_name）を取得
            role = serializer.validated_data.get('role')

            group_name = None
            groups = parent_user.groups.all()
            for group in groups:
                if group.name.startswith(family_name):
                    group_name = group.name
                    break

            # 新しいユーザーにファミリーネーム（family_name）を設定
            user.family_name = family_name
            user.save()

            # ファミリーネームのグループを取得または作成
            family_group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(family_group)

            if role == 'parent':
                parent_group_name = "Parents"
                parent_group, created = Group.objects.get_or_create(name=parent_group_name)
                parent_user.groups.add(parent_group)
            elif role == 'child':
                child_group_name = "Children"
                child_group, created = Group.objects.get_or_create(name=child_group_name)
                user.groups.add(child_group)

                # PocketMoney インスタンスを作成
                pocket_money = PocketMoney(
                    child=user,
                    group=group_name,
                    amount=0.00,  # 初期金額を設定
                    date=timezone.now().date(),  # 現在の日付を設定
                    transaction_type=PocketMoney.DEPOSIT,  # 初期トランザクションタイプを設定
                    memo='Initial deposit'  # メモを設定
                )
                pocket_money.save()

            return Response({"message": "User account created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChildrenInFamilyView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name='Parents').exists():
            return User.objects.none()

        family_group = None
        for group in user.groups.all():
            if group.name != 'Parents':
                family_group = group
                break

        if not family_group:
            return User.objects.none()

        children_group = Group.objects.get(name='Children')
        return User.objects.filter(groups=family_group).filter(groups=children_group)

class ChildPocketMoneyView(generics.RetrieveAPIView):
    serializer_class = PocketMoneySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        child_id = self.kwargs.get('child_id')
        return User.objects.get(id=child_id)

    def retrieve(self, request, *args, **kwargs):
        child = self.get_object()
        pocket_money_records = PocketMoney.objects.filter(child=child)
        total_amount = pocket_money_records.aggregate(
            total=Sum(
                Case(
                    When(transaction_type=PocketMoney.DEPOSIT, then='amount'),
                    When(transaction_type=PocketMoney.WITHDRAWAL, then=-1 * F('amount')),
                    output_field=DecimalField()
                )
            )
        )['total']

        job_cards = JobCard.objects.filter(child=child)
        job_reports = JobReport.objects.filter(reported_by=child)
        withdrawal_requests = WithdrawalRequest.objects.filter(reported_by=child)

        return Response({
            'child': UserSerializer(child).data,
            'pocket_money_records': PocketMoneySerializer(pocket_money_records, many=True).data,
            'total_amount': total_amount,
            'job_cards': JobCardSerializer(job_cards, many=True).data,
            'job_reports': JobReportSerializer(job_reports, many=True).data,
            'withdrawal_requests': WithdrawalRequestSerializer(withdrawal_requests, many=True).data,
        })
    
    def delete(self, request, *args, **kwargs):
        child = self.get_object()
        job_card_id = self.kwargs.get('job_card_id')
        
        job_card = get_object_or_404(JobCard, id=job_card_id, child=child)
        job_card.delete()
    
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateJobCardView(generics.CreateAPIView):
    serializer_class = JobCardSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Parents').exists():
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            children = serializer.validated_data.get('child')
            job_name = serializer.validated_data.get('job_name')
            money = serializer.validated_data.get('money')
            job_image = serializer.validated_data.get('job_image')

            family_group = request.user.groups.exclude(name='Parents').first()

            for child in children:
                JobCard.objects.create(
                    child=child,
                    group=family_group.name,
                    job_name=job_name,
                    money=money,
                    job_image=job_image
                )
            
            return Response({"detail": "Job cards created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalJobRequestView(generics.UpdateAPIView):
    serializer_class = JobReportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Parents').exists():
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        job_report_id = self.kwargs.get('job_report_id')
        job_report = get_object_or_404(JobReport, id=job_report_id)

        PocketMoney.objects.create(
            child=job_report.reported_by,
            group=job_report.group,
            amount=job_report.money,
            date=timezone.now().date(),
            transaction_type=PocketMoney.DEPOSIT,
            memo=job_report.job_name
        )

        job_report.delete()

        return Response({"detail": "Job report approved successfully."}, status=status.HTTP_200_OK)


class ApprovalWithdrawalRequestView(generics.UpdateAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Parents').exists():
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        withdrawal_request_id = self.kwargs.get('withdrawal_request_id')
        withdrawal_request = get_object_or_404(WithdrawalRequest, id=withdrawal_request_id)

        PocketMoney.objects.create(
            child=withdrawal_request.reported_by,
            group=withdrawal_request.group,
            amount=withdrawal_request.money,
            date=timezone.now().date(),
            transaction_type=PocketMoney.WITHDRAWAL,
            memo=withdrawal_request.title
        )

        withdrawal_request.delete()

        return Response({"detail": "Withdrawal request approved successfully."}, status=status.HTTP_200_OK)
    
############# Children Views ##############

class ChildDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Parents').exists():
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        child = request.user
        pocket_money_records = PocketMoney.objects.filter(child=child)
        total_amount = pocket_money_records.aggregate(total=Sum(
            Case(
                When(transaction_type=PocketMoney.DEPOSIT, then='amount'),
                When(transaction_type=PocketMoney.WITHDRAWAL, then=-1 * F('amount')),
                output_field=IntegerField()
            )
        ))['total']

        return Response({'total_amount': total_amount})

class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        child = request.user
        job_cards = JobCard.objects.filter(child=child)
        serializer = JobCardSerializer(job_cards, many=True)
        return Response({'job_cards': serializer.data})

class ReportJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(JobCard, id=job_id)
        user = request.user

        family_group = None
        for group in user.groups.all():
            if group.name != 'Children':
                family_group = group

        JobReport.objects.create(
            job_name=job.job_name,
            money=job.money,
            group=family_group,
            reported_by=user,
        )

        return Response({"detail": f"Job {job.job_name} has been reported for approval."}, status=status.HTTP_201_CREATED)

class CreateWithdrawalRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        family_group = None
        for group in user.groups.all():
            if group.name != 'Parents':
                family_group = group

        serializer = WithdrawalRequestSerializer(data=request.data)
        if serializer.is_valid():
            withdrawal_request = serializer.save(reported_by=user, group=family_group)
            return Response({'detail': 'Withdrawal request created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
