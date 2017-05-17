#check whether email has right format or not
def checkEmail(email):
	match=re.search(r'\w+@\w+',email)
	if match:
		return True
	else:
		return False

#passwordMD5Hash
#import hashlib
def hashPassword(password):
	m=hashlib.md5()
	password=password.encode('utf-8')
	m.update(password)
	return m.hexdigest()
