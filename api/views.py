from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
# Create your views here.
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"Passed for {request.user.email}!")


from rest_framework import generics
from rest_framework.decorators import api_view

from .models import Task, List
from .serializers import TaskSerializer, ListSerializer

#
# @api_view(['GET'])
class TaskList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    # queryset = Task.objects.all()
    def get_queryset(self):
        queryset = Task.objects.all()
        list = self.request.query_params.get('taskList')
        user_request = self.request.user
        if user_request is not None:
            queryset = queryset.filter(user=user_request)
        if list is not None:
            queryset = queryset.filter(taskList=list)
        return queryset
    def perform_create(self, serializer):
        # Atribuie utilizatorul autentificat listei
        try:
            list_instance = serializer.validated_data['taskList']
        except :
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)
        if list_instance.user != self.request.user:
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        ##mi-o verifica acolo nu aici wtf
        #deci pun validatori de
    


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        queryset = List.objects.all()
        user_request = self.request.user
        if user_request is not None:
            queryset = queryset.filter(user=user_request)
        return queryset

class ListList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListSerializer
    queryset = List.objects.all().filter()
    def get_queryset(self):
        queryset = List.objects.all()
        user_request = self.request.user
        if user_request is not None:
            print("Ceva nu e none")
            queryset = queryset.filter(user=user_request)
        else:
            print("Ceva")
        return queryset

    def perform_create(self, serializer):
        # Atribuie utilizatorul autentificat listei
        serializer.save(user=self.request.user)

class ListDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListSerializer
    def get_queryset(self):
        queryset = List.objects.all()
        user_request = self.request.user
        if user_request is not None:
            queryset = queryset.filter(user=user_request)
        return queryset
