from flask import Flask, render_template
import json
import urllib.request as request
import ssl

app = Flask(__name__)


api_key = '18983e10f268a5371158020929510bfe'
base_url = 'https://api.themoviedb.org/3/'+'search/movie?api_key='+api_key+'&query='+'fight'


@app.route('/')
def index():
	ssl._create_default_https_context =  ssl._create_unverified_context
	conn = request.urlopen(base_url)
	json_data = json.loads(conn.read())
	return render_template('index.html', data=json_data['results'])

if __name__ == '__main__':
	app.run(debug=True)