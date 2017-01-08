from django.db import models
class Robot(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField(upload_to='robots')
	@classmethod
	def create(klass,name,file):
		robot = klass(name=name,file=file)
		return robot
