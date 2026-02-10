from rest_framework import viewsets, views, request, response, exceptions, permissions, status
from .serializer import UserSerializer
from .services import create_user, user_username_selector, create_token
from django.db import IntegrityError
from . import authentication


class RegisterApi(views.APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            create_user(user_dc=serializer.validated_data)

        except IntegrityError:
            return response.Response(
                {"error": "Username or email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return response.Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response.Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


#class RegisterApi(views.APIView):
 #   def post(self, request):
  #      serializer = UserSerializer(data=request.data)
   #     serializer.is_valid(raise_exception=True)
    #    data = serializer.validated_data
     #   serializer.instance = create_user(user_dc=data)
      #  return response.Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LoginApi(views.APIView):
    permission_classes = []
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = user_username_selector(username=username)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = create_token(user_id=user.id)
        resp = response.Response(status=status.HTTP_200_OK)
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp



class UserApi(views.APIView):
    """
    this endpoint can only be used
    if the user is authenticated
    """
    authentication_classes = (authentication.CustomAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return response.Response(serializer.data)



class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "so long farewell"}
        return resp



