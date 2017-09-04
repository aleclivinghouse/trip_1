from __future__ import unicode_literals

from django.db import models
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
############BASIC VALIDATIONS############
#email must be of format
#name must have a length of at least 4
#password and password_conf need to match

class UserManager(models.Manager):
	def validate_reg(self, post_data):
		#create a dictionary for a user
		a_user = {}
		#create a dictionary for the errors
		errors = {}
		##name validation
		if len(post_data['name']) < 3:
			##if there is a name error in the user dictionary
			errors['name'] = "Name must be at least 3 characters long"
		if len(post_data['user_name']) < 3:
			errors['user_name'] = "User name must be at least 3 characters long"
		###email validation
		if not re.match(EMAIL_REGEX, post_data['email'] ):
				errors['email'] = "Email must be in the proper format"
		####password comfirmation
		if len(post_data['password']) < 8:
			errors['name'] = "Password must be at least 8 characters long"
		if post_data['password'] != post_data['password_conf']:
			errors['password'] = "Password must match password confirmation "
		print errors
		return errors

class DestinationManager(models.Manager):
	def basic_validator(self, post_data):
		errors = {}
		if len(post_data['dest_name']) < 1:
			##if there is a name error in the user dictionary
			errors['dest_name'] = "Name must not be empty"
		if len(post_data['description']) < 1:
			errors['description'] = "Description must not be empty"

		if len(post_data['start_date']) < 1:
			errors['start_date'] = "Start Date must not be empty"

		if len(post_data['end_date']) < 1:
			errors['end_date'] = "End Date must not be empty"
		if str(post_data['start_date']) < str(datetime.date.today()):
			errors['start_date'] = "Travel Start Date must be today or later"
		if str(post_data['end_date']) < str(post_data['start_date']):
			errors['end_date'] = "Travel Start Date must be today or later"
		if errors:
			return errors
		else:
			pass
# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255, default="")
	user_name = models.CharField(max_length=255, default="")
	email = models.CharField(max_length=255, default="")
	password = models.CharField(max_length=255, default="")
	date_hired = models.CharField(max_length=255, default="")
	###replace the default manager with your custom manager
	objects = UserManager()


class Destination(models.Model):
	dest_name = models.CharField(max_length=255, default="")
	description = models.TextField(default="")
	start_date = models.DateTimeField(auto_now_add = True)
	end_date = models.DateTimeField(auto_now_add = True)
	planned_by = models.ForeignKey(User)
	objects = DestinationManager()

class Middle(models.Model):
	user = models.ForeignKey(User)
	destination = models.ForeignKey(Destination)
