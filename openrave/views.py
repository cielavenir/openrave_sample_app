from openrave.models import Robot
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from . import openrave_env

import openravepy
import base64,time,json
import StringIO
import sys

def array2URL(data):
	import PIL ###
	mode = 'RGB'
	size = data.shape[1],data.shape[0]
 	img = PIL.Image.frombuffer(mode, size, data.tostring(), 'raw', mode, 0, 1)
	buf = StringIO.StringIO()
	img.save(buf,format='PNG')
	return 'data:image/png;base64,'+base64.b64encode(buf.getvalue())

# Create your views here.
def index(request,f_json=False):
	resp=StringIO.StringIO()
	robots=Robot.objects.all()
	robots_for_render=[]
	with openrave_env:
		for e in robots:
			openrave_env.LoadData(e.file)
			robot=openrave_env.GetRobots()[0]
			if f_json:
				robot_info={'id':e.name,'name':robot.GetName(),'jobs':robot.GetDOF()}
			else:
				robot_info="[%s] %s, jobs=%d"%(e.name,robot.GetName(),robot.GetDOF())
			try:
				I=openrave_env.GetViewer().GetCameraImage(640,480,openrave_env.GetViewer().GetCameraTransform(),[640,640,320,240])
				if f_json:
					robot_image=array2URL(I)
				else:
					robot_image='<li><img src="'+array2URL(I)+'"></li>'
			except Exception as detail:
				sys.stderr.write(str(type(detail))+"\n")
				sys.stderr.write(str(detail)+"\n")
				robot_image=''
			openrave_env.Remove(robot)
			robots_for_render.append({'info':robot_info,'image':robot_image})
	if f_json:
		return HttpResponse(json.dumps(robots_for_render))
	else:
		return render(request,'index.html',{'num_robots':len(robots),'robots':robots_for_render})

def info(request):
	return index(request,True)

@csrf_exempt
def add(request,robot_name=''):
	if not robot_name:
		return HttpResponseBadRequest("robot_name is empty\n")
	if any(e.name==robot_name for e in Robot.objects.all()):
		return HttpResponseForbidden("robot_name %s already exists\n"%robot_name)
	try:
		robot_file=request.POST['file']
		try:
			env=openravepy.Environment()
			with env:
				env.LoadData(robot_file)
				robot=env.GetRobots()[0]
				q=Robot.create(robot_name,robot_file)
				q.save()
		except IndexError:
			env.Destroy()
			return HttpResponseBadRequest("robot xml is invalid (note: 'include' must be resolved)\n")
		except openravepy.openravepy_ext.openrave_exception:
			env.Destroy()
			return HttpResponseBadRequest("robot xml is invalid (note: 'include' must be resolved)\n")
		env.Destroy()
		return HttpResponse("added [%s]\n"%robot_name)
	except KeyError:
		return HttpResponseBadRequest("file param not specified\n")

def remove(request,robot_name=''):
	q=get_object_or_404(Robot,name=robot_name)
	q.delete()
	return HttpResponse("removed [%s]\n"%robot_name)
