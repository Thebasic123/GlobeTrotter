
#not sure what user._id is in user.js

#most of those variables were used in login function,
#I wrote my python login version myself, I did't use those.

#var mongoose = require('mongoose');
#var crypto = require('crypto');
#var express = require('express');
#var router = express.Router();
#var User = mongoose.model('user');


import hashlib
def login(HttpRequest,HttpResponse):
	if request.method != 'POST':
		raise Http404('Only POSTs are allowed')
	try:
		m = Member.objects.get(email=request.POST['email'])
		if m.password == request.POST['pass']:
			request.session['member_id'] = m.id
			return HttpResponseRedirect('/you-are-logged-in/')
	except Member.DoesNotExist:
		return HttpResponse("Your username and password didn't match.")

def logout(HttpRequest,HttpResponse):
	try:
		del HttpRequest.session['user']
		del HttpRequest.session['member_id']
	except KeyEoor:
		pass
	return HttpResponse('You are logged out.')

def register(HttpRequest,HttpResponse):
	email=HttpRequest.POST['email']
	password=request.POST['pass']
	passconfirm=request.POST['passconfirm']
	if(not checkEmail(email)): #if email has wrong format
		return HttpResponse("Your email address's format is incorrect")
	if(password.len() < 6): #if user password is too short
		return HttpResponse('Your password is too short,it should be longger than 6 characters.')
	else:
		if(confirmPassword(password,passconfirm)):
			hashedPassword=hashPassword(password)
			#create a new dict for user account
			newUser={'email':email,'password':hashedPassword}
			HttpRequest.session['user']=email
			HttpRequest.session['member_id']=newUser.id ###not sure about this line
			return HttpResponse('Congratulation!!! You have signed up!')


		else:
			return HttpResponse('Your password must be same with your confirm passowrd')


def checkEmail(email): # check whether email is right format or not
	match=re.search(r'\w+@\w+',email)
	if match:
		return True
	else:
		return False


#check whether password is same with confirmPassword or not
def confirmPassword(pass, passconfirm):
	if(pass == passconfirm):
		return True
	else:
		return False

#use MD5 hash password
def hashPassword(password):
	m=hashlib.md5()
	password=password.encode('utf-8')
	m.update(password)
	return m.hexdigest()


#I don't know how to convert this line
#module.exports = router;