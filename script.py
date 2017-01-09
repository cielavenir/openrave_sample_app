#!/usr/bin/python
import sys,httplib,urllib
from contextlib import closing

def add_robot(host,robot_name,robot_content):
	with closing(httplib.HTTPConnection(host)) as http:
		http.request('POST','/add/'+robot_name,urllib.urlencode({'file':robot_content}),{'Content-type':"application/x-www-form-urlencoded"})
		return http.getresponse().read()

def remove_robot(host,robot_name):
	with closing(httplib.HTTPConnection(host)) as http:
		http.request('GET','/remove/'+robot_name)
		return http.getresponse().read()

if __name__=='__main__':
	if len(sys.argv)<4:
		sys.stderr.write("script host[:port] robot_name [filepath.xml|--remove]\n")
		sys.stderr.write("note: filepath.xml must be complete.\n")
		sys.stderr.write("If it includes something else, use `openrave -save complete.xml partial.xml` prior.\n")
		sys.exit(1)
	host=sys.argv[1]
	robot_name=sys.argv[2]
	robot_file=sys.argv[3]
	if robot_file!='--remove':
		with open(robot_file) as f:
			robot_file=f.read()
	http=httplib.HTTPConnection(sys.argv[1])
	if robot_file=='--remove':
		sys.stdout.write(remove_robot(host,robot_name))
	else:
		sys.stdout.write(add_robot(host,robot_name,robot_file))
