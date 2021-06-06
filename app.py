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
import re
from http import cookies
import pyodbc

server = 'localhost'
username = 'NimaFaghihi'
password = 'Nima1234'
database = 'SearchFLIX'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


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

def get_recommendations(movie_id):
    '''
    Rekommenderar film baserat på filmid - Ali & Nima & Axel
    '''
    return('https://api.themoviedb.org/3/movie/{}/recommendations?api_key='+api_key+'&language=en-US&page=1').format(movie_id)

def get_query_string(movie_id, country):
    ''' 
    Hämtar query från användare
    '''
    return {'country':country,'tmdb_id':'movie/{}'.format(movie_id)}
 
def get_movie_URL(movie_id):
    '''
    Hämtar movie URL
    '''
    return ('https://api.themoviedb.org/3/movie/{}?api_key='+api_key+'&language=en-US').format(movie_id)

def get_movie_credits(movie_id):
    '''
    Hämtar film credits - Ali & Nima
    '''
    return ('https://api.themoviedb.org/3/movie/{}/credits?api_key='+api_key+'&language=en-US').format(movie_id)


 
headers = {
    'x-rapidapi-key': rapid_api_key,    
    'x-rapidapi-host': 'streaming-availability.p.rapidapi.com'
    }
 
@app.route('/app')
def search_function(): 
    '''
    Hämtar användarens input från sökfunktionen i index.html för att sedan göra en sökning med hjälp av API. - Ali & Nima
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
    Route för att hämta information och tillgänglighet för film. - ALi
    '''
    country = (request.args.get('country') or "se").lower() # Hämtar land från get parametern or default se(Sverige)
    ssl._create_default_https_context =  ssl._create_unverified_context
    conn = requests.urlopen(get_movie_URL(movie_id))
    json_data = json.loads(conn.read())
    network = rq.request('GET', url, headers=headers, params=get_query_string(movie_id, country))
    conn2 = requests.urlopen(get_movie_credits(movie_id))
    conn3 = requests.urlopen(get_recommendations(movie_id))
    json_data2 = json.loads(conn2.read())
    json_data3 = json.loads(conn3.read())
    return render_template('movie.html', data=json_data, network_data=json.loads(network.text), data2=json_data2, data3=json_data3, country=country)

@app.route('/faq')
def faq(): 
    '''
    Route för FAQ-sidan
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('faq.html')
 
@app.route('/')
def index(): 
    '''
    Route för startsidan
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('index.html')

 
@app.route('/contact')
def contact(): 
    '''
    Route för kontakt-sidan
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('contact.html')

@app.route('/about_us')
def about_us(): 
    '''
    Route för about-us sidan
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('aboutUs.html')

@app.route('/instructions')
def instructions(): 
    '''
    Route för instruktions-sida
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('instructions.html')
 
@app.route('/top_rated_movies')
def topMovie_function(): 
    '''
    Funktion för att generera top 10 filmer. - Ali
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    conn = requests.urlopen(topMovie_url)
    json_data = json.loads(conn.read())
    return render_template('topMovies.html', data=json_data['results'])
 
@app.route('/top_netflix')
def top_netflix(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för Netflix - Ali
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topNetflix.html')


@app.route('/top_prime')
def top_prime(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för Prime - Ali
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topPrime.html')

@app.route('/top_hbo')
def top_hbo(): 
    '''
    Funktion som hämtar och presenterar en top 10 lista för HBO - Ali
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topHBO.html')

@app.route('/top_disney')
def top_disney():
    '''
    Funktion som hämtar och presenterar en top 10 lista för Disney - Ali
    '''
    ssl._create_default_https_context =  ssl._create_unverified_context
    return render_template('topDisney.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
    '''
    Funktion som låter användare logga in  - Nima & Axel
    '''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = cnxn.cursor()
        cursor.execute('SELECT * FROM new_user1 WHERE username = ? AND password = ?', username, password)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
        
            session['username'] = username
            msg = 'Logged in successfully !'
            return render_template('profile.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    '''
    Funktion som låter användare logga ut  - Nima & Axel
    '''
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))
  

@app.route('/register', methods =['GET', 'POST'])
def register():
    '''
    Funktion som låter användare skapa konto om sådant inte redan finns - Nima & Axel
    '''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = cursor = cnxn.cursor()
        cursor.execute('SELECT * FROM new_user1 WHERE username = ?', username)
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO new_user1 ( username, password, email) VALUES ( ?, ?, ?)', (username, password, email, ))
            cnxn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return redirect(url_for('index'))
    return render_template('register.html', msg = msg)



if __name__ == '__main__':
    app.run(debug=True)
 
 
 
