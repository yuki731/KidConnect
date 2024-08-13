from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import UserSignupSerializer, LoginSerializer

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
        # トークンの生成は別途設定が必要
        # 例: from rest_framework.authtoken.models import Token
        # token, created = Token.objects.get_or_create(user=user)
        return Response({'token': 'your_generated_token'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
