class Result:
	SUCCESS_CODE = 0
	FAIL_CODE = 1
	
	def __int__(self, code, message, data):
		self.code = code
		self.message = message
		self.data = data