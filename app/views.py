from django.shortcuts import render, redirect
from .forms import VolunteerForm
import requests
from decouple import config
from newsapi import NewsApiClient
from .models import Volunteer, FireStation
from datetime import datetime
import tweepy
from textblob import TextBlob


def home(request):
	api = NewsApiClient(api_key=config('newsAPI'))
	all_articles = api.get_everything(q='blaze', language='en', sort_by='relevancy')
	publisher = {}
	for article in all_articles['articles']:
		if article['source']['name'] not in publisher and article['content'] is not None:
			publisher[article['source']['name']] = {'url': '', 'content': '', 'title': '', 'image': ''}
			publisher[article['source']['name']]['url'] = article['url']
			publisher[article['source']['name']]['content'] = article['content']
			publisher[article['source']['name']]['title'] = article['title']
			publisher[article['source']['name']]['image'] = article['urlToImage']

	auth = tweepy.OAuthHandler(config('consumer_key'), config('consumer_secret'))
	auth.set_access_token(config('access_token'), config('access_token_secret'))
	api = tweepy.API(auth)

	tweets = api.search('mumbai fire casualties', count=5)
	texts = ''
	for tweet in tweets:
		texts += str(TextBlob(tweet.text)) + ' || '
	return render(request, 'app/home.html', {'publisher': publisher, 'texts': texts})


def show_volunteers(request):
	if request.method == 'POST':
		visitor_area = request.POST.get('area')
		volunteer_list = Volunteer.objects.filter(area=visitor_area)
	else:
		volunteer_list = Volunteer.objects.all()
	return render(request, 'app/volunteer.html', {'volunteer_list': volunteer_list})


def register(request):
	if request.method == 'POST':
		form = VolunteerForm(request.POST, request.FILES)
		if form.is_valid():
			volunteer = form.save(commit=False)
			volunteer.picture = request.FILES['picture']
			volunteer.save()
			return redirect('/app/volunteers')
	else:
		form = VolunteerForm()
	return render(request, 'app/register.html', {'form': form})


def directions(request, pk):
	if request.method == 'POST':
		user_location = request.POST.get('user_loc')
		volunteers = Volunteer.objects.get(pk=pk)
		addr = volunteers.address.replace(' ', '+')

		url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(addr, config('google_key'))
		geodata = requests.get(url).json()
		destination1 = geodata['results'][0]['geometry']['location']
		destination = [destination1['lat'], destination1['lng']]

		now = datetime.now()
		context = {
			'start': user_location.split(','),
			'end': destination,
			'time': now
		}
		return render(request, 'app/test2.html', context)
	return render(request, 'app/location.html')


def directions2(request, pk):
	if request.method == 'POST':
		user_location = request.POST.get('user_loc')
		station = FireStation.objects.get(pk=pk)
		addr = station.address.replace(' ', '+')

		url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(addr, config('google_key'))
		geodata = requests.get(url).json()
		destination1 = geodata['results'][0]['geometry']['location']
		destination = [destination1['lat'], destination1['lng']]

		now = datetime.now()
		context = {
			'start': user_location.split(','),
			'end': destination,
			'time': now
		}
		return render(request, 'app/test2.html', context)
	return render(request, 'app/location.html')


def centres(request):
	stations = FireStation.objects.all()
	return render(request, 'app/centre.html', {'stations': stations})


def markers(request):
	fire_stations = FireStation.objects.all()
	locs = []

	for station in fire_stations:
		addr = station.address.replace(' ', '+')
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(addr, config('google_key'))
		geodata = requests.get(url).json()
		destination1 = geodata['results'][0]['geometry']['location']
		locs.append([destination1['lat'], destination1['lng'], station.name])

	return render(request, 'app/marker.html', {'locations': locs})


def safety(request):
	return render(request, 'app/safety.html')
