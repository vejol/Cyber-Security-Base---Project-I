from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account, Event
from django.db.models import Q
import sqlite3
	
@login_required
def transferView(request):
	to = User.objects.get(username=request.GET.get('to'))
	amount = int(request.GET.get('amount'))
	message = request.GET.get("message")

	# # FIX 3 - Make 3 lines above to use POST method instead of GET method. Corrected lines are:
	# to = User.objects.get(username=request.POST.get('to'))
	# amount = int(request.POST.get('amount'))
	# message = request.POST.get("message")

	request.user.account.balance -= amount
	to.account.balance += amount

	request.user.account.save()
	to.account.save()
	
	Event.objects.create(
		sender=request.user.username, 
		receiver=to.username, 
		amount=amount,
		message=message
		)
	
	return redirect('/')


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})

@login_required
def checkView(request):
	name = request.POST.get("name")
	
	sql = "SELECT * FROM pages_event WHERE sender='"+ name + "' AND receiver='" + request.user.username + "'"
	conn = sqlite3.connect('server/db.sqlite3')
	cursor = conn.cursor()
	events = cursor.execute(sql).fetchall()
	
	## FIX 4 - Replace four lines above with these two line below:
	#result = Event.objects.filter(Q(sender=name) & Q(receiver=request.user))
	#events = [[e.id, e.sender, e.receiver, e.amount, e.message] for e in result]

	return render(request, 'pages/answer.html', {'name': name, 'events': events})

@login_required
def transactionsView(request, name):
	
	## FIX 5 - uncomment two lines below:
	#if name != request.user.username:
	#	return redirect('/')
	
	events = Event.objects.filter(
		Q(sender=name) | 
		Q(receiver=name))
	return render(request, 'pages/transactions.html', {'events': events})