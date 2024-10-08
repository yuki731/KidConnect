from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import CustomUser, PocketMoney, JobCard, JobReport, WithdrawalRequest

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'family_name', 'first_name')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['family_name', 'first_name', 'birthdate', 'address', 'icon', 'password']

    def create(self, validated_data):
        family_name = validated_data.pop('family_name')
        first_name = validated_data.pop('first_name')
        password = validated_data.pop('password')
        icon = validated_data.pop('icon', None)  # アイコンが提供されているか確認

        # ユーザーを作成
        user = CustomUser(
            family_name=family_name,
            first_name=first_name,
            **validated_data
        )
        user.set_password(password)
        
        if icon:  # アイコンが提供されていれば設定
            user.icon = icon
            
        user.save()

        # グループ名を生成してグループを作成
        group_name = f"{family_name}_{user.id}"
        group, created = Group.objects.get_or_create(name=group_name)
        group_parents, _ = Group.objects.get_or_create(name='Parents')

        # ユーザーをグループに追加
        user.groups.add(group)
        user.groups.add(group_parents)
        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError({'detail': 'Invalid credentials'})
        return data


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birthdate', 'address', 'family_name', 'first_name', 'groups']

    def get_groups(self, obj):
        # ユーザーが所属するグループ名のリストを返す
        return [group.name for group in obj.groups.all()]

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('parent', 'Parent'), ('child', 'Child')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password', 'role', 'birthdate', 'address']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            birthdate=validated_data.get('birthdate'),
            address=validated_data.get('address')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PocketMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketMoney
        fields = ('id', 'child', 'group', 'amount', 'aproved_by', 'date', 'transaction_type', 'memo')

class JobCardListSerializer(serializers.ModelSerializer):
    child = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name='Children'),  # groups フィールドでフィルタリング
        many=True
    )

    class Meta:
        model = JobCard
        fields = ['id', 'child', 'group', 'job_name', 'money', 'job_image']

class JobCardSerializer(serializers.ModelSerializer):
    child = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name='Children'),  # groups フィールドでフィルタリング
        many=False
    )

    class Meta:
        model = JobCard
        fields = ['id', 'child', 'group', 'job_name', 'money', 'job_image']

class JobListSerializer(serializers.ModelSerializer):
    child = serializers.StringRelatedField()  # または他の適切なフィールドタイプ

    class Meta:
        model = JobCard
        fields = ['id', 'child', 'group', 'job_name', 'money', 'job_image']


class JobReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReport
        fields = ('id', 'job_name', 'money', 'group', 'reported_by', 'reported_at', 'status')

class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ('id', 'title', 'money', 'group', 'reported_by', 'reported_at', 'status')
        read_only_fields = ('group', 'reported_by', 'reported_at', 'status')
