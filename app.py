from flask import Flask, render_template, request
import json
import urllib.request as requests
import urllib.parse
import ssl
import cgi

app = Flask(__name__)

#api från themoviedb.com

import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')



api_key = '18983e10f268a5371158020929510bfe' # Vår authentication key. 
base_url = 'https://api.themoviedb.org/3/'+'search/movie?api_key='+api_key+'&query='+'fight' #temporär url endast för test. 
search_URL = 'https://api.themoviedb.org/3/'+'search/movie?api_key='+api_key+'&query=' #Sök URL för vårt API. 


'''Hämtar användarens input från sökfunktionen i index.html för att sedan göra en sökning med hjälp av API. '''

@app.route('/app')
def search_function(): 
	search = request.args.get('searchbox')
	ssl._create_default_https_context =  ssl._create_unverified_context
	search = urllib.parse.quote(search)
	conn = requests.urlopen(search_URL+search)
	json_data = json.loads(conn.read())
	return render_template('index.html', data=json_data['results'])

''' Temporär startsida för att spike-testa API'''

@app.route('/')
def index(): #temporär test sida för att pröva API
	ssl._create_default_https_context =  ssl._create_unverified_context
	conn = requests.urlopen(base_url)
	json_data = json.loads(conn.read())
	return render_template('index.html', data=json_data['results'])

if __name__ == '__main__':
	app.run(debug=True)