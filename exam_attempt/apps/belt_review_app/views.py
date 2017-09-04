from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from time import gmtime, strftime
import bcrypt


def index(request):
	return render(request, 'belt_review_app/index.html')

def dashboard(request):
	context = {
	#get the middles where the user id
	"users_trip": Middle.objects.filter(user__id = request.session['user_id']),
	"others_trip":Middle.objects.exclude(user__id = request.session['user_id'])
	}
	return render(request, 'belt_review_app/dashboard.html', context)

def addtrip(request):

	return render(request, 'belt_review_app/addtrip.html')


#these are the process routes
def add(request):
	errors = Destination.objects.basic_validator(request.POST)
	if errors:
		##for the exact error
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/addtrip')
	else:
		pass
		current_user = User.objects.get(id = request.session['user_id'])
		the_dest = Destination.objects.create(dest_name = request.POST['dest_name'], description = request.POST['description'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], planned_by = current_user)
		the_user = User.objects.get(id = request.session['user_id'])
		Middle.objects.create(user = the_user, destination = the_dest)
		return redirect('/dashboard')

def adduser(request, id):
	#the id is the destination id
	the_destination = Destination.objects.get(id = id)
	current_user = User.objects.get(id = request.session['user_id'])
	Middle.objects.create(user = current_user, destination = the_destination)
	return redirect("/dashboard")

# def showuser(request, id):
# 	count = 0
# 	reviewNum = Review.objects.filter(user__id = id).all()
# 	for x in reviewNum:
# 		count = count + 1
# 	context = {
# 	"the_user": User.objects.get(id = id),
# 	"reviews": Review.objects.filter(user__id = id).all(),
# 	"count": count
# 	}
# 	return render(request, 'belt_review_app/showuser.html', context)



def showtrip(request, id):
	context = {
	"trip": Middle.objects.get(id = id),
	"users_going": Middle.objects.filter(destination__id = id)
	}
	return render(request, 'belt_review_app/showtrip.html', context)


################################################################################################################################################
def logout(request):
	request.session['user_id'] = 0
	return redirect('/main')


def register(request):
	###below comes from validate_reg in models.Manager
	errors = User.objects.validate_reg(request.POST)
	if errors:
		##for the exact error
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/main')
	else:
		####if the user has entered successfully log them in
		pass
		found_users = User.objects.filter(email=request.POST['email'])
		if found_users.count() > 0:
			##display an error if the email has already been taken
			messages.error(request, "email already taken", extra_tags="email")
			return redirect('/main')
		else:
			#register the user
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			created_user = User.objects.create(name=request.POST['name'], user_name =request.POST['user_name'], email=request.POST['email'], password=hashed_pw)
			request.session['user_id'] = created_user.id
			request.session['user_name'] = created_user.name
			print created_user
			return redirect('/dashboard')
		return redirect('/main')
def login(request):
	###se if email is in the database
	found_users = User.objects.filter(email=request.POST['email'])
	if found_users.count() > 0:
		#check passwords
		found_user = found_users.first()
		if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
			#we are logged in
			request.session['user_id'] = found_user.id
			request.session['user_name'] = found_user.name
			print found_user
			return redirect('/dashboard')
		else:
			messages.error(request, "Login Failed", extra_tags="email")
			return redirect('/main')
	else:
		messages.error(request, "Login Failed", extra_tags="email")
		return redirect('/main')
