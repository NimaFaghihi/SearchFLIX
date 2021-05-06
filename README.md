#  SearchFLIX

** Version 1.0 **


# Projektbeskrivning:

Searchflix är en webbapplikation som är skapad för att samla utbudet av filmer från dem olika streamingtjänsterna. Använderen har i dagsläget möjlighet att söka på en film för att sedan få fram information om vart filmen kan streamas. I en kommande version kommer användaren även att ha möjlighet till att filtrera vilket land hen befinner sig i för att filtrera utbudet per land. 

# Testa vår hemsida

http://searchflix.pythonanywhere.com/

# Instruktioner för API nyckel.

För att köra vår kod behövs två API nycklar. 

api_key från https://www.themoviedb.org/documentation/api 

samt

rapid_api_key från https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability

API nyckeln behöver sedans sparas som api_key.cfg med följande format:

[KEYS]
api_key: #########

rapid_api_key : #########

# Instruktioner för att köra kod

steg 1.
Installera flask
http://flask.palletsprojects.com/en/1.1.x/installation/


steg 2. 
Installera requests genom att skriva följande i python terminalen:
pip3 install requests

Extrahera samtliga filer från .zip filen till flask mappen och kör flask.

# Github
https://github.com/NimaFaghihi/SearchFLIX

