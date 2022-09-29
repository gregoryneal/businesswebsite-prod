from http.client import responses
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from hashlib import md5

from businesswebsite.settings import COMPANY_NAME, DEBUG, USE_CART
from .models import FAQEntry, KnowledgeBaseEntry
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as LOGIN, logout as LOGOUT
from .templatetags.service_extras import GetMarkdownObject

from django.core import mail
import traceback

def services(request):
	if (request.method != "GET"):
		return redirect('error', status_code=405)
		
	template = loader.get_template("service2.html")
	return contextLoader({}, request, template)

def requestQuote(request):	
	template = loader.get_template('request_quote.html')
	context = {}
	if (request.method == "POST"):
		quoteForm = QuoteForm(request.POST, request.FILES)
		#pprint.pprint(str(quoteForm.errors))
		if (quoteForm.is_valid()):
			if emailFormToAdmin(request, quoteForm, "Quote Form Submission"):
				# Delete the cart cookies since the email sent successfully
				return redirect('thanks')
			else:
				return contactError(request)
		else:
			# Pass through 
			for error in quoteForm.errors:
				print("ERROR: " + str(error))

	elif (request.method == "GET"):
		quoteForm = QuoteForm()
	else:
		return redirect('error', status_code=405)
		
	context.update({'quote_form': quoteForm})
	return contextLoader(context, request, template)

def contact(request):
	context = {}
	template = loader.get_template('contact_form.html')

	# If we posted to / it was the contact form, process it.
	if (request.method == "POST"):
		# New instance of ContactForm pre filled with POSTed data
		contactForm = ContactForm(request.POST)
		# Validate it
		if (contactForm.is_valid()):
			print("Contact form valid!")
			context = {}
			if (emailFormToAdmin(request, contactForm, "Contact Form Submission")):
				return redirect('thanks')
			else: 
				return redirect('contact-error')
		else:
			# Pass through the very end and return the form again
			# But with errors attached this time
			for error in contactForm.errors:
				print("ERROR: " + str(error))
	# We are receiving GET request
	elif (request.method == "GET"):
		contactForm = ContactForm()

	# Update the context with however we made the contact form
	context.update({"quote_form":contactForm})
	return contextLoader(context, request, template)

#This is where they always hit first
def blank(request):
	return redirect(services)

def school(request):
	if (request.method == 'GET'):
		template = loader.get_template('k-base.html')
		school = KnowledgeBaseEntry.objects.all()
		context = {'kbase':school}
		return contextLoader(context, request, template)
	else:
		return redirect('error', status_code=405)

def article(request, slug):
	template = loader.get_template('article.html')
	entry = KnowledgeBaseEntry.objects.get(slug=slug)
	context = {'entry':entry}
	return contextLoader(context, request, template)

def about(request):
	template = loader.get_template('about.html')
	return contextLoader({}, request, template)

def faq(request):
	template = loader.get_template('faq.html')
	faq = FAQEntry.objects.all()
	context = {
		'num_entries': len(faq),
		'entries': faq,
		}
	return contextLoader(context, request, template)

def login(request):
	if (request.method == 'POST'):
		r = request.POST
		# Someone is trying to login, lets verify the credentials
		print("we just received a POST request to login view.")
		name = r.get("username")
		pwd = r.get("password")
		user = authenticate(request, username=name, password=pwd)

		if user is not None:
			# The user is authenticated, they can now purchase things
			print("Authenticated!")
			LOGIN(request, user)
		else:
			# User is not authenticated, tell the browser with javascript.
			print("Not authenticated!")
			return redirect('index')
	#return redirect('index')
		if (request.META['HTTP_REFERER']):
			return redirect(request.META['HTTP_REFERER'])
		else:
			return redirect('index')
	else: 
		# 405: Method not Allowed
		return redirect('error', status_code=405)

@login_required
def logout(request):
	# Logout through Django backend
	LOGOUT(request)
	return redirect('index')

def register(request):
	if (request.method == "POST"):
		register = RegisterForm(request.POST)
		if (register.is_valid()):
			user = register.save()
			LOGIN(request, user)
			return redirect('profile')
		else:
			print("Error validating registration request!")
			print("Error: " + str(register.errors))
			return redirect('register-error')
	return redirect('index')

def registerError(request, form=None):
	template = loader.get_template('register-error.html')
	context = {}
	if (form != None): context = {'register_form':form}
	return contextLoader(context, request, template)

def currentUserProfile(request):
	if (request.method == "GET"):
		user = getattr(request, "user", None)
		if not getattr(user, "is_authenticated", True):
			return redirect('error', status_code=403)
		else:
			gravatar_id = md5(bytes(user.email.strip().lower(), 'utf-8')).hexdigest()
			context = {
				'gravatar_id': gravatar_id,
				'user': user,
			}
			template = loader.get_template('profile.html')
			return contextLoader(context, request, template)
	else:
		return redirect('error', status_code=405)

def contactThanks(request):
	template = loader.get_template('thanks.html')
	context = {}
	context["email_success"] = True
	return contextLoader(context, request, template)

def contactError(request):	
	template = loader.get_template('thanks.html')
	context = {}
	context["email_success"] = False
	context["quote_form"] = QuoteForm(request.POST, request.FILES)
	return contextLoader(context, request, template)

# Dynamically generate status code pages
def errorPage(request, status_code):	
	template = loader.get_template('error-code.html')

	header = "Hmm, you aren't supposed to see this."
	if (100 < status_code < 200):
		header = "Hold up!"
	elif (200 < status_code < 300):
		header = "You missed something!"
	elif (300 < status_code < 400):
		header = "Get up on out of here!"
	elif (400 < status_code < 500):
		header = "You broke it :("
	elif (500 < status_code):
		header = "I broke :("

	reason = responses.get(status_code, "Unknown Status Code")
	if (status_code == 418): reason = "I'm a teapot"
	if (status_code == 420): reason = "Enhance your calm"
	context = {
		'status_header': header,
		'status_code': status_code,
		'status_reason': reason
	}

	return errorContextLoader(context, request, template, status_code=status_code)



#######################################
##                                   ##
## HELPER FUNCTIONS BELOW THIS POINT ##
##                                   ##
#######################################
# Adds all the context that we want on every page before loading the template
def contextLoader(context, request, template=None, status_code=200):
	if (template == None):
		template = loader.get_template('base.html')

	# These here in case a login or register form is passed
	# to this with errors, we dont accidentally delete it
	if (not hasattr(context, 'login_form')): context.update({'login_form': LoginForm()})
	if (not hasattr(context, 'register_form')): context.update({'register_form': RegisterForm()})
	
	context.update({
					'company_name': COMPANY_NAME,
					'debug': DEBUG,
					'canonical_path': request.build_absolute_uri(request.path),
				})
	response = HttpResponse(template.render(context, request))
	response.status_code = status_code
	return response

def errorContextLoader(context, request, template=None, status_code=200):
	if (template == None):
		template = loader.get_template('base.html')
	context.update({'login_form': LoginForm(),
					'register_form': RegisterForm(),
					'use_cart': USE_CART,
					'company_name': COMPANY_NAME,
					'debug': DEBUG,
					'canonical_path': request.build_absolute_uri(request.path),
				})
	response = HttpResponse(template.render(context, request))
	response.status_code = status_code
	return response

def emailFormToAddresses(request, form, recipients, subject=None):
	print("Emailing form to addresses!")
	# Assumes address is a valid email address
	if not form.is_valid(): 
		#print(form.errors)
		return False
	data = form.cleaned_data
	try:
		# c -> Email body in string form that will be emailed to the addresses
		c = "New request from customer: \n\n"
		if (request.user.is_authenticated):
			c += "Sent by logged in user:\nUsername: \t" + request.user.username
			if (request.user.first_name != ""):
				c += "\nFirst name: " + request.user.first_name
			else:			
				c += "\nFirst name: (not set)"
			if (request.user.last_name != ""):
				c += "\nLast name: " + request.user.last_name
			else:
				c += "\nLast name: (not set)"
			if (request.user.email != ""):
				c += "\nEmail: " + request.user.email
			else:
				c += "\nEmail: (not set)"
			c += "\n\n"
			
		for k in list(data.keys()):
			if (k == "images"):
				continue
			# Uppercase the key name
			l = k[0].upper() + k[1:]
			# Append the string to a new line of the email
			c += l + ": " + str(data[k]) + "\n"
		
		s = "RMOE Contact Form Query"
		if (subject != None):
			s = subject
		message = mail.EmailMessage(s, c, "admin@rmoverlandelectrical.com", recipients)

		if (request.FILES):
			c = "Images: "
			i = 1
			for k in list(request.FILES.getlist("images")):
				print(k)
				print("name: %s"%k.name)
				print("size: %s"%k.size)
				print("type: %s"%k.content_type)
				print("type extras: %s"%k.content_type_extra)
				print("multiple chunks: %s"%k.multiple_chunks())

				filetype = k.name[-4:]
				ctype = k.content_type
				# Reset the content_type of the image
				# based on the file type
				if (filetype == "jpg"):
					ctype = k.content_type = "image/jpeg"
				elif (filetype == "png"):
					ctype = k.content_type = "image/png"
				
				c += k.name + ", "
				message.attach(k.name, k.read())		
			message.body += c
		success = message.send()
		print(success)
		#yagmail.SMTP('gregcraig25').send(subject="RMOE Contact Form Query", contents=c, to=recipients)
		return bool(success)
	except:
		print("Failed to email form:\n")
		print(traceback.print_exc())
		return False

def emailFormToAdmin(request, form, subject=None):
	# Emails just to myself
	admin = ['gregcraig25@gmail.com', 'tlim.mines@gmail.com']
	return emailFormToAddresses(request, form, admin, subject)
	
