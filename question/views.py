from django.shortcuts import render, render_to_response
from forms import LocationForm
import requests
import json

def home(request):
	status = {
		'comma': "Learn how to type! City COMMA State.",
		'error': "I don't know what you did wrong. I can't find it.",
		'sports': "Things are gonna suck because of a game.",
		'maybe': "Probably, but not due to a sports game."
	}

	if request.method == 'POST':
		form = LocationForm(request.POST, request.FILES)

		if form.is_valid():
			cd = form.cleaned_data
			if ',' in cd['location']:

				# Split the location in two, seperated with a comma.
				location = cd['location'].split(',')
				city = location[0]
				state = location[1]

				# Call the API with a request
				r = requests.get('http://api.espn.com/v1/sports/events/venues?apikey=ngac5qbzrdxnxakjwb46fd3m')
				things = json.loads(r.text)
				return render_to_response('index.html', {'status':status['maybe']})
			else:
				form = LocationForm()
				return render(request, 'index.html', {'status':status['comma'], 'form':form})
		else:
			form = LocationForm()
			return render(request, 'index.html', {'status':status['error'], 'form':form})
	form = LocationForm()
	return render(request, 'index.html', {'form':form})
