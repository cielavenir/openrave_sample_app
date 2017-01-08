from django.test import TestCase

class RobotTest(TestCase):
	def test_add(self):
		response=self.client.post('/add/test',{'file':''})
		self.failUnlessEqual(response.status_code,200)
	def test_remove(self):
		pass

