from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

#Regsiter API

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context = self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#LoginAPI
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format = None)
    
#GetUserAPI
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
#ChangePasswordAPI
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset = None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)

        if(serializer.is_valid()):
            if(not self.object.check_password(serializer.data.get("old_password"))):
                return Response({"old_password": ["Wrong password"]}, status = status.HTTP_400_BAD_REQEUST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password Updated Successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status.HTTP_400_BAD_REQEUST)
