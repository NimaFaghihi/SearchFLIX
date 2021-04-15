from flask import Flask, render_template, request
import json
import urllib.request as requests
import urllib.parse
import ssl
import cgi
import requests as rq
import configparser


app = Flask(__name__, static_url_path='/static')

#api från themoviedb.com

import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')

cfg = configparser.ConfigParser()
cfg.read('api_key.cfg')
api_key = cfg.get('KEYS', 'api_key', raw='')
rapid_api_key = cfg.get('KEYS', 'rapid_api_key', raw='')

#api_key = '18983e10f268a5371158020929510bfe' # Vår authentication key. 
base_url = 'https://api.themoviedb.org/3/'
search_URL = 'https://api.themoviedb.org/3/'+'search/multi?api_key='+api_key+'&query=' #Sök URL för vårt API. 
movie_URL = 'https://api.themoviedb.org/3/movie/155?api_key='+api_key+'&language=en-US'
topMovie_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=18983e10f268a5371158020929510bfe&language=en-US&page=1'


'''Hämtar användarens input från sökfunktionen i index.html för att sedan göra en sökning med hjälp av API. '''

url = "https://streaming-availability.p.rapidapi.com/get/basic"

querystring = {"country":"us","tmdb_id":"movie/155"}


headers = {
    'x-rapidapi-key': rapid_api_key,
    'x-rapidapi-host': "streaming-availability.p.rapidapi.com"
    }

@app.route('/app')
def search_function(): 
	'''
	Hämtar användarens input från sökfunktionen i index.html för att sedan göra en sökning med hjälp av API.
	'''
	search = request.args.get('searchbox')
	ssl._create_default_https_context =  ssl._create_unverified_context
	search = urllib.parse.quote(search)
	conn = requests.urlopen(search_URL+search)
	json_data = json.loads(conn.read())
	return render_template('search.html', data=json_data['results'])

@app.route('/movie/155')
def test(): 
	'''
	Test route för att hämta streaming tillgänglighet för film. 
	'''
	ssl._create_default_https_context =  ssl._create_unverified_context
	conn = requests.urlopen(movie_URL)
	json_data = json.loads(conn.read())
	network = rq.request("GET", url, headers=headers, params=querystring)
	return render_template('movie.html', data=json_data, network_data=json.loads(network.text))

@app.route('/test')
def test_function(): 
	'''
	Test route för att hämta streaming tillgänglighet för film. 
	'''
	ssl._create_default_https_context =  ssl._create_unverified_context
	network = rq.request("GET", url, headers=headers, params=querystring)
	return render_template('test.html', network_data=json.loads(network.text))

@app.route('/')
def index(): 
	ssl._create_default_https_context =  ssl._create_unverified_context
	return render_template('index.html')

@app.route('/Top_rated_movies')
def topMovie_function(): 
	'''
	Funktion för att generera top 20 filmer.
	'''
	search = request.args.get('searchbox')
	ssl._create_default_https_context =  ssl._create_unverified_context
	search = urllib.parse.quote(search)
	conn = requests.urlopen(topMovie_url)
	json_data = json.loads(conn.read())
	return render_template('topMovies.html', data=json_data['results'])

if __name__ == '__main__':
	app.run(debug=True)



	'''file = open("resp_text.json", "w")
	file.write(conn.text)
	file.close()
	file = open("resp_content.json", "w")
	file.write(conn.text)
	file.close()
	with open('resp_content.json') as json_file:
		json_data = json.loads(json_file.read())'''