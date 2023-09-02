from rest_framework import serializers
from django.contrib.auth.models import User
from .models import List, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        User._meta.get_field('email')._unique = True
        User._meta.get_field('email').blank = False
        User._meta.get_field('email').null = False
        fields = ['id', 'username', 'password', 'email']


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'listName']
        # fields = ('__all__')
        # fields = ['listName']

    def validate(self, data):
        #aici nu vreau validare
        list_instance = data.get('listName')
        #asta ii numele listei
        # print(data)
        # print(list_instance)
        # user_request = self.context['request'].taskList
        # print(user_request)
        # if list_instance.user != user_request:
        #     raise serializers.ValidationError("Lista nu apartine")
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = ['id']
        fields = ['id', 'taskName', 'taskDetails', 'taskList', 'taskDue', 'taskPriority', 'taskDone']
        # fields += 'id'

    def __init__(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)
        user_request = self.context['request'].user
        self.fields['taskList'].queryset = List.objects.filter(user=user_request)
        #BUN ASA

    def validate(self, data):
        list_instance = data.get('taskList')
        user_request = self.context['request'].user
        if list_instance is not None:
            if list_instance.user != user_request:
                raise serializers.ValidationError("Lista selectată nu aparține utilizatorlui autentificat.")
        return data
