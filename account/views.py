from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import MyUser
from account.serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data  # данные прилетают в data, а не в POST
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):  # был у форм
            serializer.save()
            # perform.create()
            return Response('Successfully registered on StackOverFlow14!', status=201)


class ActivateView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = MyUser.objects.filter(phone_number=phone_number, activation_code=code).first()
        # filter вернет queryset, поэтому используем first
        if not user:
            return Response('No such user', status=400)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('You have successfully activated your account', status=200)
