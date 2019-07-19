from django.shortcuts import render
from django.http import HttpResponse

industries = [
	{
		'name' : 'Hotels',
		'index' : 1,
		'prominence' : 8
	},
	{
		'name' : 'Airlines',
		'index' : 2,
		'prominence' : 10
	}
]

critical = [
	{
		'name' : 'The Monarch Luxur',
		'issues' : ['Cold water', 'Hot water', 'No ventilation']
	},
	{
		'name' : 'Conrad Bengaluru',
		'issues' : ['yes','no','yeah']
	}
]


def home(request):
	context = {
		'indu' : industries 
	}
	return render(request, 'mil/home.html', context)

def landing(request):
	return render(request, 'mil/index.html')

def interface(request):
	return render(request, 'mil/interface.html')

def issues_h(request):
	all_issues = {
		'crit' : critical
	}
	return render(request, 'mil/hotel_issues.html', all_issues)