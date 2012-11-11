from django.shortcuts import render, render_to_response
from forms import LocationForm
import requests
import json

def home(request):
	status = {
		'comma': "Learn how to type! City COMMA State.",
		'error': "I don't know what you did wrong. I can't find it.",
		'sports': "Things are gonna suck because of a game in town.",
		'maybe': "Probably, but not due to a sports game."
	}

	if request.method == 'POST':
		form = LocationForm(request.POST, request.FILES)

		if form.is_valid():
			cd = form.cleaned_data
			if ',' in cd['location']:

				# Split the location in two, seperated with a comma.
				location = cd['location'].split(',')
				city = location[0].upper()
				state = location[1].upper()

				# Call the API with a request
				if espn(city, state):
					return render_to_response('index.html', {'status':status['sports']})
				return render_to_response('index.html', {'status':status['maybe']})
			else:
				form = LocationForm()
				return render(request, 'index.html', {'status':status['comma'], 'form':form})
		else:
			form = LocationForm()
			return render(request, 'index.html', {'status':status['error'], 'form':form})
	form = LocationForm()
	return render(request, 'index.html', {'form':form})


def espn(given_city, given_state):
	r = requests.get('http://api.espn.com/v1/sports/events/venues?apikey=ngac5qbzrdxnxakjwb46fd3m')
	nice = json.loads(r.text)


	sports = nice['sports']

	a_leagues = ['NBA', 'NFL', 'MLB', 'NHL']
	l_events = []
	for each in sports:
		for name in each['leagues']:

			if name['shortName'] in a_leagues:
				temp = each['leagues']
				l_events.append(each['leagues'])

	for league in l_events:
		for thing in league:
			events = thing['events']
			for event in events:
				city = event['venues'][0]['city']
				if city == given_city:
					return True
	return False
