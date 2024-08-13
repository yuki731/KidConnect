from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .models import PocketMoney, JobCard, JobReport, WithdrawalRequest

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'birthdate', 'address', 'family_name', 'first_name')

    def create(self, validated_data):
        family_name = validated_data.pop('family_name')
        first_name = validated_data.pop('first_name')
        password = validated_data.pop('password')
        
        # ユーザーを作成
        user = User(
            **validated_data,
            family_name=family_name,
            first_name=first_name
        )
        user.set_password(password)
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
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'birthdate', 'address', 'family_name')

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('parent', 'Parent'), ('child', 'Child')])

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'birthdate', 'address']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
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

class JobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = ('id', 'child', 'group', 'job_name', 'money', 'job_image')

class JobReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReport
        fields = ('id', 'job_name', 'money', 'group', 'reported_by', 'reported_at', 'status')

class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ('id', 'title', 'money', 'group', 'reported_by', 'reported_at', 'status')