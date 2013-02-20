from django.shortcuts import render, render_to_response
from forms import LocationForm
#import requests
#import json

import urllib
from datetime import date
import calendar
from bs4 import BeautifulSoup
#beautiful soup stuff to get web scraped info

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

				# Split the location in two, separated with a comma.
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

def sports(given_city, given_state):
        day = str(date.today().day)
        
	#START NBA
        soup_nba = BeautifulSoup(urllib.urlopen('http://aol.sportingnews.com/nba/schedule'))
        #create the current day's arena list populated with arena names
	curr_day_nba_list = []
        num_lines = 1
        for each in soup_nba.find_all('th'):
                if day in each.get_text():
                        for item in each.find_parent('table').find_all('td'):
                            num_lines += 1
                            if num_lines % 5 == 0:
                                    curr_day_nba_list.append(item.text)
        #static dictionary of NBA arenas created on 1/19/13
        nba_arenas = {
                'Air Canada Centre': {'city':'Toronto', 'state':'ON'},
                'American Airlines Arena': {'city':'Miami','state':'FL'},
                'American Airlines Center': {'city':'Dallas', 'state':'TX'},
                'Amway Center': {'city':'Orlando', 'state':'FL'},
                'AT&T Center': {'city':'San Antonio', 'state':'TX'},
                'Bankers Life Fieldhouse': {'city':'Indianapolis', 'state':'IN'},
                'Barclays Center': {'city':'Brooklyn', 'state':'NY'},
                'BMO Harris Bradley Center': {'city':'Milwaukee', 'state':'WI'},
                'Chesapeake Energy Arena': {'city':'Oklahoma City', 'state':'OK'},
                'EnergySolutions Arena': {'city':'Salt Lake City', 'state':'UT'},
                'FedExForum': {'city':'Memphis', 'state':'TN'},
                'Madison Square Garden': {'city':'Manhattan', 'state':'NY'},
                'New Orleans Arena': {'city':'New Orleans', 'state':'LA'},
                'Oracle Arena': {'city':'Oakland', 'state':'CA'},
                'Pepsi Center': {'city':'Denver', 'state':'CO'},
                'Philips Arena': {'city':'Atlanta', 'state':'GA'},
                'Quicken Loans Arena': {'city':'Cleveland', 'state':'OH'},
                'Rose Garden': {'city':'Portland', 'state':'OR'},
                'Sleep Train Arena': {'city':'Sacramento', 'state':'CA'},
                'Staples Center': {'city':'Los Angeles', 'state':'CA'},
                'Target Center': {'city':'Minneapolis', 'state':'MN'},
                'TD Garden': {'city':'Boston', 'state':'MA'},
                'The Palace of Auburn Hills': {'city':'Detroit', 'state':'MI'},
                'Time Warner Cable Arena': {'city':'Charlotte', 'state':'NC'},
                'Toyota Center': {'city':'Houston', 'state':'TX'},
                'United Center': {'city':'Chicago', 'state':'IL'},
                'US Airways Center': {'city':'Phoenix', 'state':'AZ'},
                'Verizon Center': {'city':'Washington D.C.', 'state':''},
                'Wells Fargo Center': {'city':'Philadelphia', 'state':'PA'},
        }
        #force users to use state abbreviations!
        cities_dict = {}
        for key in nba_arenas.keys():
                for item in curr_day_nba_list:
                        if key == item:
                                cities_dict[nba_arenas[key]['city']] = nba_arenas[key]['state']
        for city in cities_dict.keys():
                print city.upper(), cities_dict[city].upper()
                if given_city == city.upper(): #and given_state == cities_dict[city].upper():
                        return True
        #END NBA
        #works until location information is deleted

        #START NHL
        soup_nhl = BeautifulSoup(urllib.urlopen('http://aol.sportingnews.com/nhl/schedule'))
        curr_day_nhl_list = []
        num_lines = 1
        for each in soup_nhl.find_all('th'):
                if day in each.get_text():
                        for item in each.find_parent('table').find_all('td'):
                                num_lines += 1
                                if num_lines % 5 == 0:
                                        curr_day_nhl_list.append(item.text)
        #check to make sure arena names match with schedule...!!!
        #also check abbreviations of canadian states
        nhl_arenas = {
                'Air Canada Centre': {'city':'Toronto', 'state':'ON'},
                'American Airlines Center': {'city':'Dallas', 'state':'TX'},
                'BB&T Center': {'city':'Sunrise', 'state':'FL'},
                'Bell Centre': {'city':'Montreal', 'state':'QC'},
                'Bridgestone Arena': {'city':'Nashville', 'state':'TN'},
                'Consol Energy Center': {'city':'Pittsburgh', 'state':'PA'},
                'First Niagara Center': {'city':'Buffalo', 'state':'NY'},
                'Honda Center': {'city':'Anaheim', 'state':'CA'},
                'HP Pavilion at San Jose': {'city':'San Jose', 'state':'CA'},
                'Jobing.com Arena': {'city':'Glendale', 'state':'AZ'},
                'Joe Louis Arena': {'city':'Detroit', 'state':'MI'},
                'Madison Square Garden': {'city':'New York City', 'state':'NY'},
                'MTS Centre': {'city':'Winnipeg', 'state':'MB'},
                'Nassau Veterans Memorial Coliseum': {'city':'Uniondale', 'state':'NY'},
                'Nationwide Arena': {'city':'Columbus', 'state':'OH'},
                'Pepsi Center': {'city':'Denver', 'state':'CO'},
                'PNC Arena': {'city':'Raleigh', 'state':'NC'},
                'Prudential Center': {'city':'Newark', 'state':'NJ'},
                'Rexall Place': {'city':'Edmonton', 'state':'AB'},
                'Rogers Arena': {'city':'Vancouver', 'state':'BC'},
                'Scotiabank Place': {'city':'Ottawa', 'state':'ON'},
                'Scotiabank Saddledome': {'city':'Calgary', 'state':'AB'},
                'Scottrade Center': {'city':'St. Louis', 'state':'MO'},
                'Staples Center': {'city':'Los Angeles', 'state':'CA'},
                'Tampa Bay Times Forum': {'city':'Tampa Bay', 'state':'FL'},
                'TD Garden': {'city':'Boston', 'state':'MA'},
                'United Center': {'city':'Chicago', 'state':'IL'},
                'Verizon Center': {'city':'Washington D.C.', 'state':''},
                'Wells Fargo Center': {'city':'Philadelphia', 'state':'PA'},
                'Xcel Energy Center': {'city':'Saint Paul', 'state':'MN'},  
        }
        cities_dict = {}
        for key in nhl_arenas.keys():
                for item in curr_day_nhl_list:
                        if key == item:
                                cities_dict[nhl_arenas[key]['city']] = nhl_arenas[key]['state']
        for city in cities_dict.keys():
                if given_city == city.upper(): #and given_state == cities_dict[city].upper():
                        return True
        #END NHL

        #START MLB
        soup_mlb = BeautifulSoup(urllib.urlopen('http://aol.sportingnews.com/mlb/schedule'))
        #create the current day's arena list populated with arena names
        curr_day_mlb_list = []
        num_lines = 1
        for each in soup_mlb.find_all('th'):
            if day in each.get_text():
                for item in each.find_parent('table').find_all('td'):
                    num_lines += 1
                    if num_lines % 5 == 0:
                        curr_day_mlb_list.append(item.text)
        mlb_arenas = {
                'Dodger Stadium': {'city':'Los Angeles', 'state':'CA'},
                'Coors Field': {'city':'Denver', 'state':'CO'},
                'Yankee Stadium': {'city':'New York City', 'state':'NY'},
                'Turner Field': {'city':'Atlanta', 'state':'GA'},
                'Rogers Centre': {'city':'Toronto', 'state':'ON'},
                'Chase Field': {'city':'Phoenix', 'state':'AZ'},
                'Rangers Ballpark in Arlington': {'city':'Arlington', 'state':'TX'},
                'Safeco Field': {'city':'Seattle', 'state':'WA'},
                'Oriole Park at Camden Yards': {'city':'Baltimore', 'state':'MD'},
                'Angel Stadium of Anaheim': {'city':'Anaheim', 'state':'CA'},
                'Busch Stadium': {'city':'St. Louis', 'state':'MO'},
                'Citizens Bank Park': {'city':'Philadelphia', 'state':'PA'},
                'Progressive Field': {'city':'Cleveland', 'state':'OH'},
                'PETCO Park': {'city':'San Diego', 'state':'CA'},
                'Great American Ball Park': {'city':'Cincinnati', 'state':'OH'},
                'Citi Field': {'city':'New York City', 'state':'NY'},
                'AT&T Park': {'city':'San Francisco', 'state':'CA'},
                'Miller Park': {'city':'Milwaukee', 'state':'WI'},
                'Nationals Park': {'city':'Washington D.C.', 'state':''},
                'Comerica Park': {'city':'Detroit', 'state':'MI'},
                'Wrigley Field': {'city':'Chicago', 'state':'IL'},
                'Minute Maid Park': {'city':'Houston', 'state':'TX'},
                'U.S. Cellular Field': {'city':'Chicago', 'state':'IL'},
                'Target Field': {'city':'Minneapolis', 'state':'MN'},
                'PNC Park': {'city':'Pittsburgh', 'state':'PA'},
                'Kauffman Stadium': {'city':'Kansas City', 'state':'MO'},
                'Fenway Park': {'city':'Boston', 'state':'MA'},
                'Marlins Park': {'city':'Miami', 'state':'FL'},
                'Oakland-Alameda County Coliseum': {'city':'Oakland', 'state':'CA'},
                'Tropicana Field': {'city':'St. Petersburg', 'state':'FL'},
        }
        cities_dict = {}
        for key in mlb_arenas.keys():
                for item in curr_day_mlb_list:
                        if key == item:
                                cities_dict[mlb_arenas[key]['city']] = mlb_arenas[key]['state']
        for city in cities_dict.keys():
                if given_city == city.upper(): #and given_state == cities_dict[city].upper():
                        return True
        #END MLB

        #START NFL
        soup_nfl = BeautifulSoup(urllib.urlopen('http://aol.sportingnews.com/nfl/schedule'))
        curr_day_nfl_list = []
        num_lines = 1
        for each in soup_nfl.find_all('th'):
                if day in each.get_text():
                        for item in each.find_parent('table').find_all('td'):
                                num_lines += 1
                                if num_lines % 5 == 0:
                                        curr_day_nfl_list.append(item.text)
        nfl_arenas = {
                'FedEx Field': {'city':'Landover', 'state':'MD'},
                'MetLife Stadium': {'city':'East Rutherford', 'state':'NJ'},
                'Cowboys Stadium': {'city':'Arlington', 'state':'TX'},
                'Arrowhead Stadium': {'city':'Kansas City', 'state':'MO'},
                'Sports Authority Field as Mile High': {'city':'Denver', 'state':'CO'},
                'Sun Life Stadium': {'city':'Miami Gardens', 'state':'FL'},
                'Bank of America Stadium': {'city':'Charlotte', 'state':'NC'},
                'Mercedes-Benz Superdome': {'city':'New Orleans', 'state':'LA'},
                'FirstEnergy Stadium': {'city':'Cleveland', 'state':'OH'},
                'Lambeau Field': {'city':'Green Bay', 'state':'WI'},
                'Ralph Wilson Stadium': {'city':'Orchard Park', 'state':'NY'},
                'Georgia Dome': {'city':'Atlanta', 'state':'GA'},
                'Reliant Stadium': {'city':'Houston', 'state':'TX'},
                'M&T Bank Stadium': {'city':'Baltimore', 'state':'MD'},
                'Qualcomm Stadium': {'city':'San Diego', 'state':'CA'},
                'Candlestick Park': {'city':'San Francisco', 'state':'CA'},
                'Lincoln Financial Field': {'city':'Philadelphia', 'state':'PA'},
                'LP Field': {'city':'Nashville', 'state':'TN'},
                'Gillette Stadium': {'city':'Foxborough', 'state':'MA'},
                'EverBank Field': {'city':'Jacksonville', 'state':'FL'},
                'CenturyLink Field': {'city':'Seattle', 'state':'WA'},
                'Edward Jones Dome': {'city':'St. Louis', 'state':'MO'},
                'Raymond James Stadium': {'city':'Tampa', 'state':'FL'},
                'Paul Brown Stadium': {'city':'Cincinnati', 'state':'OH'},
                'Heinz Field': {'city':'Pittsburgh', 'state':'PA'},
                'Ford Field': {'city':'Detroit', 'state':'MI'},
                'Mall of America Field at Hubert H. Humphrey Metrodome': {'city':'Minneapolis', 'state':'MN'},
                'University of Phoenix Stadium': {'city':'Glendale', 'state':'AZ'},
                'Oakland-Alameda County Coliseum': {'city':'Oakland', 'state':'CA'},
                'Lucas Oil Stadium': {'city':'Indianapolis', 'state':'IN'},
                'Soldier Field': {'city':'Chicago', 'state':'IL'},
                'Rogers Centre': {'city':'Toronto', 'state':'ON'},
                'Aloha Stadium': {'city':'Honolulu', 'state':'HI'},
                'Fawcett Stadium': {'city':'Canton', 'state':'OH'},
        }
        cities_dict = {}
        for key in nfl_arenas.keys():
                for item in curr_day_nfl_list:
                        if key == item:
                                cities_dict[nfl_arenas[key]['city']] = nfl_arenas[key]['state']
        for city in cities_dict.keys():
                if given_city == city.upper(): #and given_state == cities_dict[city].upper():
                        return True
        #END NFL
                
	return False


#to do list:
#date ranges
#state specific
#list which league is playing
