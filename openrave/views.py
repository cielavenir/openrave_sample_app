from openrave.models import Robot
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def add(request,robot_name=''):
    return HttpResponse("add [%s] not implemented yet"%robot_name)

def remove(request,robot_name=''):
    return HttpResponse("remove [%s] not implemented yet"%robot_name)

