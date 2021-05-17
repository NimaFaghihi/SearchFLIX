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
 
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')
 
cfg = configparser.ConfigParser()
cfg.read('api_key.cfg')
api_key = cfg.get('KEYS', 'api_key', raw='')
rapid_api_key = cfg.get('KEYS', 'rapid_api_key', raw='')
 
base_url = 'https://api.themoviedb.org/3/'
search_URL = 'https://api.themoviedb.org/3/search/movie?api_key='+api_key+'&query=' #Sök URL för vårt API. 
topMovie_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key='+api_key+'&language=en-US'
 
 
url = 'https://streaming-availability.p.rapidapi.com/get/basic'
 
def getQueryString(movie_id):
    return {'country':'se','tmdb_id':'movie/{}'.format(movie_id)}
 
def getMovieURL(movie_id):
    return ('https://api.themoviedb.org/3/movie/{}?api_key='+api_key+'&language=en-US').format(movie_id)

def getMovieCredits(movie_id):
    return ('https://api.themoviedb.org/3/movie/{}/credits?api_key='+api_key+'&language=en-US').format(movie_id)

 
headers = {
    'x-rapidapi-key': rapid_api_key,    
    'x-rapidapi-host': 'streaming-availability.p.rapidapi.com'
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
 
@app.route('/movie/<movie_id>')
def movie_details(movie_id): 
    '''
    Test route för att hämta streaming tillgänglighet för film. 
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    conn = requests.urlopen(getMovieURL(movie_id))
    json_data = json.loads(conn.read())
    network = rq.request('GET', url, headers=headers, params=getQueryString(movie_id))
    conn2 = requests.urlopen(getMovieCredits(movie_id))
    json_data2 = json.loads(conn2.read())
    return render_template('movie.html', data=json_data, network_data=json.loads(network.text), data2=json_data2)



@app.route('/faq')
def faq(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('faq.html')
 
@app.route('/')
def index(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('index.html')

 
@app.route('/contact')
def contact(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('contact.html')
 
@app.route('/top_rated_movies')
def topMovie_function(): 
    '''
    Funktion för att generera top 20 filmer.
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    conn = requests.urlopen(topMovie_url)
    json_data = json.loads(conn.read())
    return render_template('topMovies.html', data=json_data['results'])
 
@app.route('/top_netflix')
def top_netflix(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topNetflix.html')


@app.route('/top_prime')
def top_prime(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topPrime.html')

@app.route('/top_hbo')
def top_hbo(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topHBO.html')

@app.route('/top_disney')
def top_disney():
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topDisney.html')

if __name__ == '__main__':
    app.run(debug=True)
 
 
 
