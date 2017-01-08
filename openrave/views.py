from openrave.models import Robot
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import openravepy
import base64
import StringIO

def array2URL(data):
	mode = 'RGB'
	size = data.shape[1],data.shape[0]
 	img = PIL.Image.frombuffer(mode, size, data.tostring(), 'raw', mode, 0, 1)
	buf = StringIO.StringIO()
	img.save(buf,format='PNG')
	return 'data:image/png;base64,'+base64.b64encode(buf.getvalue())

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
			robot=env.GetRobots()[-1]
			resp.write("[%s] jobs=%d<br>"%(e.name,robot.GetDOF()))
			try:
				import PIL.Image ###
				I=env.GetViewer().GetCameraImage(640,480,env.GetViewer().GetCameraTransform(),[640,640,320,240])
				resp.write('<img src="'+array2URL(I)+'"><br>')
			except:
				pass
		resp.write("</body></html>")
	env.Destroy()
	return HttpResponse(resp.getvalue())

@csrf_exempt
def add(request,robot_name=''):
	if not robot_name:
		return HttpResponse("robot_name is empty\n")
	if any(e.name==robot_name for e in Robot.objects.all()):
		return HttpResponse("robot_name %s already exists\n"%robot_name)
	try:
		robot_file=request.POST['file']
		q=Robot.create(robot_name,robot_file)
		q.save()
		return HttpResponse("added [%s]\n"%robot_name)
	except KeyError:
		return HttpResponse("file param not specified\n")

def remove(request,robot_name=''):
	q=get_object_or_404(Robot,name=robot_name)
	q.delete()
	return HttpResponse("removed [%s]\n"%robot_name)

