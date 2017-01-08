#!/usr/bin/python
import sys,httplib,urllib
if len(sys.argv)<4:
	sys.stderr.write("script host[:port] robot_name [filepath|--remove]")
	sys.exit(1)

robot_name=sys.argv[2]
robot_file=sys.argv[3]
if robot_file!='--remove':
	with open(robot_file) as f:
		robot_file=f.read()

http=httplib.HTTPConnection(sys.argv[1])
if robot_file=='--remove':
	http.request('GET','/remove/'+robot_name)
else:
	http.request('POST','/add/'+robot_name,urllib.urlencode({'file':robot_file}),{'Content-type':"application/x-www-form-urlencoded"})

sys.stdout.write(http.getresponse().read())
