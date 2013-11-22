from django.shortcuts import render, render_to_response
from forms import LocationForm

import urllib
from datetime import date
import calendar
from bs4 import BeautifulSoup 
# Beautiful soup stuff to get web scraped info

import arenas

day = str(date.today().day)

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
                # Split the location in two, separated with a comma
		location = cd['location'].split(',')
		city = location[0].upper()
		state = location[1].upper()
		# Call the sports function with a request
		if sports(city, state):
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

def load_curr_arenas(url):
    soup = BeautifulSoup(urllib.urlopen(url))
    # Create the current day's arena list populated with arena names
    curr_day_list = []
    num_lines = 1
    for each in soup.find_all('th'):
        if day in each.get_text():
            for item in each.find_parent('table').find_all('td'):
                num_lines += 1
                if num_lines % 5 == 0:
                    curr_day_list.append(item.text) 
    return curr_day_list

def check_for_games(given_city, given_state):
    url_list = [
        'http://aol.sportingnews.com/nba/schedule',
        'http://aol.sportingnews.com/nhl/schedule',
        'http://aol.sportingnews.com/mlb/schedule',
        'http://aol.sportingnews.com/nfl/schedule',
    ]
    for url in url_list:
        curr_day_list = load_curr_arenas(url)   
        if curr_day_list:
            if 'nba' in url:
                arenas_dict = arenas.nba_arenas
            elif 'nhl' in url:
                arenas_dict = arenas.nhl_arenas
            elif 'mlb' in url:
                arenas_dict = arenas.mlb_arenas
            elif 'nfl' in url:
                arenas_dict = arenas.nfl_arenas
            cities_dict = {}
            for key in arenas_dict.keys():
                for item in curr_day_list:
                    if key == item:
                        cities_dict[arenas_dict[key]['city']] = arenas_dict[key]['state']
                        for city in cities_dict.keys():
                            if given_city == city.upper():
                                return TrueStrunk and White
    return False

def sports(given_city, given_state):
    if check_for_games(given_city, given_state):
        return True
    return False

