from django.test import TestCase
from BeautifulSoup import BeautifulSoup
import zlib,base64

TRIDOF_zlib_b64='eNrFl+tumzAUx7/nKRDfE7BJtk5ykdbuIm2ZJlV7AQImcQS4MmZN3n6+YSA0hKRizcWxzzk+Nn//gg16ohvKnSLK8b0bfPn9TbXdcOY46CcpHmhyFHXxOimQ9JhuD1GJXYcfn0U9OQobiVUCFfeHRUWZRZzQIvQXvuPUBfJaLhv+HdPcpIqPGSkSzFQu42aUq/joQMoQOL54fxKZ2uZ2dJSQqpTDBiJGNxrvDpPtjksvRJ5pNN6EpGlV4keaUSZjVo4tkNd22ql7cu6ipepKuAHNPrPcP6dZ9wfRNC0xT5lILpVGXmNoevTFFtrI2fqri0Jv6MGO3V+xO5mnm6OJ/XrguOCljhMFqIc0jlHioB+UFNyJCYurLGL3LmcVdl8RakeKLVZTtXIaSWS1a5f9jL0vpPH2hUQvmoMl8nTNOjKSE14meBvOwZ3viC/yrM1GSQCV8gB5sm4deXT4i7NQcKhr1sFwSbNKySr6NK1aK6XNBZLAKUlXXXJ3vcFScwPejs3iCnD8j6sp0AFddC4iUtvBIDpgCJ1gInSWk6ADR6ID/iM6y5F3nKUiZhJuYJebi3zUdjjIDXwPbuAQN3A0Nz14nh6z6GUkPXAEPWqjmd+0Y2Gz8hYHaDCsHU0obyXWwwHJWsvc5ee60QPN4rjRZfhcliMmUGPVsGtWYX9yh7tIpGqotTuLqnYPsCrmDgdp/eAEN7HqLwbvcsFoWtugruXVjD2fnoHwKq5HoXIdqO/N6Zsxhbdguh7GdD05pvMpOEVe68FKf9CvqCDPlRCWMqNYxHLXdMVpimPhMTrZpoV9I87A5iCsqvU62oC9HLsM98DZiwSmZQIGCxRntBQrlhAmxlQnDfnf7Vl1cCtKb+EnAbPXDg1w1dvutUotTcIZ8tSDaTj7BwFUGUQ='
TRIDOF=zlib.decompress(base64.b64decode(TRIDOF_zlib_b64))

class RobotTest(TestCase):
	def test_add_invalid_robot_name(self):
		response=self.client.post('/add/',{'file':TRIDOF})
		self.failUnlessEqual(response.status_code,400)
	def test_add_no_file(self):
		response=self.client.post('/add/test_no_file',{})
		self.failUnlessEqual(response.status_code,400)
	def test_add_and_remove(self):
		response=self.client.get('/')
		self.failUnlessEqual(response.status_code,200)
		response=self.client.post('/add/test_add_and_remove',{'file':TRIDOF})
		self.failUnlessEqual(response.status_code,200)
		response=self.client.get('/')
		self.failUnlessEqual(response.status_code,200)
		response=self.client.post('/remove/test_add_and_remove')
		self.failUnlessEqual(response.status_code,200)
		response=self.client.get('/')
		self.failUnlessEqual(response.status_code,200)
		response=self.client.post('/remove/test_add_and_remove')
		self.failUnlessEqual(response.status_code,404)
	def test_remove_invalid(self):
		response=self.client.post('/remove/invalid')
		self.failUnlessEqual(response.status_code,404)

