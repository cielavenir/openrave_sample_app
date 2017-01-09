from openrave.models import Robot
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
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
	robots_for_render=[]
	env=openravepy.Environment()
	with env:
		for e in robots:
			env.LoadData(e.file)
			robot=env.GetRobots()[0]
			robot_info="[%s] %s, jobs=%d"%(e.name,robot.GetName(),robot.GetDOF())
			try:
				import PIL.Image ###
				I=env.GetViewer().GetCameraImage(640,480,env.GetViewer().GetCameraTransform(),[640,640,320,240])
				robot_image='<li><img src="'+array2URL(I)+'"></li>'
			except:
				robot_image=''
			env.Remove(robot)
			robots_for_render.append({'info':robot_info,'image':robot_image})
	env.Destroy()
	return render(request,'index.html',{'num_robots':len(robots),'robots':robots_for_render})

@csrf_exempt
def add(request,robot_name=''):
	if not robot_name:
		return HttpResponseBadRequest("robot_name is empty\n")
	if any(e.name==robot_name for e in Robot.objects.all()):
		return HttpResponseForbidden("robot_name %s already exists\n"%robot_name)
	try:
		robot_file=request.POST['file']
		q=Robot.create(robot_name,robot_file)
		q.save()
		return HttpResponse("added [%s]\n"%robot_name)
	except KeyError:
		return HttpResponseBadRequest("file param not specified\n")

def remove(request,robot_name=''):
	q=get_object_or_404(Robot,name=robot_name)
	q.delete()
	return HttpResponse("removed [%s]\n"%robot_name)

