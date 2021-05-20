'''
Importerar ramverket flask med tillhörande nödvändiga moduler
'''
from flask import ( 
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
    
)
'''
Importerar övriga nödvändiga moduler
'''
import json
import urllib.request as requests
import urllib.parse
import ssl
import cgi
import requests as rq
import configparser
from http import cookies

app = Flask(__name__, static_url_path='/static')
 
#api från themoviedb.com
 
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')
C = cookies.SimpleCookie()

cfg = configparser.ConfigParser()
cfg.read('api_key.cfg')
api_key = cfg.get('KEYS', 'api_key', raw='')
rapid_api_key = cfg.get('KEYS', 'rapid_api_key', raw='')
app.secret_key = 'somesecretkeythatonlyishouldknow'

 
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
'''
Route för FAQ-sidan
'''
def faq(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('faq.html')
 
@app.route('/')
'''
Route för startsidan
'''
def index(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('index.html')

 
@app.route('/contact')
'''
Route för kontakt-sidan
'''
def contact(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('contact.html')

@app.route('/about_us')
'''
Route för about-us sidan
'''
def about_us(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('aboutUs.html')

@app.route('/instructions')
'''
Route för instruktions-sida
'''
def instructions(): 
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('instructions.html')
 
@app.route('/top_rated_movies')
def topMovie_function(): 
    '''
    Funktion för att generera top 10 filmer.
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    conn = requests.urlopen(topMovie_url)
    json_data = json.loads(conn.read())
    return render_template('topMovies.html', data=json_data['results'])
 
@app.route('/top_netflix')
def top_netflix(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för Netflix
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topNetflix.html')


@app.route('/top_prime')
def top_prime(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för Prime
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topPrime.html')

@app.route('/top_hbo')
def top_hbo(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för HBO
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topHBO.html')

@app.route('/top_disney')
def top_disney():
    '''
    Funktion som hämtar och presenterar en top 10 lista för Disney
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topDisney.html')


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<user: {self.username}>'

users = []
users.append(User(id=1, username='Anthony', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user




@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Funktion under utveckling, skall låta användare logga in
    '''
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')




@app.route('/profile')
def profile():
    '''
    Funktion under utveckling, skall låta användare visa sin profil efter inloggning
    '''
    
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
 
 
 
