from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser
from django.contrib.auth import authenticate


class UserSignupSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'birthdate', 'address', 'family_name')

    def create(self, validated_data):
        family_name = validated_data.pop('family_name')
        
        # ユーザーを作成
        user = CustomUser.objects.create_user(**validated_data)
        
        user.family_name = family_name
        user.first_name = first_name
        
        # ユーザーIDがまだないため、グループ名は後で更新する必要があります
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