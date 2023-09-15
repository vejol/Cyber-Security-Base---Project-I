from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account, Event
from django.db.models import Q
import sqlite3


@login_required
def confirmView(request):

	# Note that this transfer is very naive
	# but will suffice for this exercise
	amount = request.session['amount']
	to = User.objects.get(username=request.session['to'])

	request.user.account.balance -= amount
	to.account.balance += amount

	request.user.account.save()
	to.account.save()
	
	print(request.user.username, 
		to.username, 
		amount,
		request.session["message"])
	
	Event.objects.create(
		sender=request.user.username, 
		receiver=to.username, 
		amount=amount,
		message=request.session["message"]
		)
	
	return redirect('/')
	

@login_required
def transferView(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = int(request.GET.get('amount'))
	request.session['message'] = request.GET.get("message")
	return render(request, 'pages/confirm.html')


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	events = Event.objects.filter(
		Q(sender=request.user) | 
		Q(receiver=request.user))
	return render(request, 'pages/index.html', {'accounts': accounts, "events": events})
