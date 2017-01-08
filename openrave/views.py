from openrave.models import Robot
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import openravepy
import StringIO

# Create your views here.
def index(request):
	resp=StringIO.StringIO()
	robots=Robot.objects.all()
	env=openravepy.Environment()
	with env:
		resp.write("<html><body>")
		resp.write("%d robots<br>"%len(robots))
		for e in robots:
			env.LoadData(e.file)
			resp.write("[%s] jobs=%d<br>"%(e.name,env.GetRobots()[-1].GetDOF()))
		resp.write("</body></html>")
	env.Destroy()
	return HttpResponse(resp)

@csrf_exempt
def add(request,robot_name=''):
	if not robot_name:
		return HttpResponse("robot_name is empty")
	if any(e.name==robot_name for e in Robot.objects.all()):
		return HttpResponse("robot_name %s already exists")
	try:
		robot_file=request.POST['file']
		q=Robot.create(robot_name,robot_file)
		q.save()
		return HttpResponse("added [%s]"%robot_name)
	except KeyError:
		return HttpResponse("file param not specified")

def remove(request,robot_name=''):
	q=get_object_or_404(Robot,name=robot_name)
	q.delete()
	return HttpResponse("removed [%s]"%robot_name)

