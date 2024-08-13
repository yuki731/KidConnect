from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.utils import timezone

from .models import CustomUser, PocketMoney
from .serializers import UserSignupSerializer, LoginSerializer, CreateUserSerializer, UserSerializer, PocketMoneySerializer, JobCardSerializer, JobReportSerializer, WithdrawalRequestSerializer

class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            # サインアップ時に新しいグループを作成し、そのグループにユーザーを追加
            user = serializer.save()

            # グループ作成とユーザー追加の成功メッセージ
            return Response({"message": "User created and added to group successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signin(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # 認証成功時にトークンを返す
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
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
                if group.name.startswith(user.family_name):
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

        group_name = None
        groups = parent_user.groups.all()
        for group in groups:
            if group.name.startswith(user.family_name):
                group_name = group.name
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