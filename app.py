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



api_key = '18983e10f268a5371158020929510bfe'
base_url = 'https://api.themoviedb.org/3/'+'search/movie?api_key='+api_key+'&query='+'fight'
search_URL = 'https://api.themoviedb.org/3/'+'search/movie?api_key='+api_key+'&query='


@app.route('/app')
def index2():
	search = request.args.get('searchbox')
	ssl._create_default_https_context =  ssl._create_unverified_context
	search = urllib.parse.quote(search)
	conn = requests.urlopen(search_URL+search)
	json_data = json.loads(conn.read())
	return render_template('index.html', data=json_data['results'])

@app.route('/')
def index():
	ssl._create_default_https_context =  ssl._create_unverified_context
	conn = requests.urlopen(base_url)
	json_data = json.loads(conn.read())
	return render_template('index.html', data=json_data['results'])

if __name__ == '__main__':
	app.run(debug=True)