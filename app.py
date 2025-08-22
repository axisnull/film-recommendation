import json
from flask import Flask, render_template, request, jsonify, session
from model import chatAI
from cosine.cosine import MovieSearcher

app = Flask(__name__)


chatbot = chatAI()
movie_search = MovieSearcher()

def chat_reply(message):
      return model.chatAI().reply(message)

# 플라스크 실행시 기본 경로
@app.route('/')
def index():
    titles, posters, genres, overviews, cast, director = movie_search.search()
    movie_info = []
    #print(type(details))
    for title, poster, genre, overview, cast, director in zip(titles, posters, genres, overviews, cast, director):
        movie_info.append({
        'title': title,
        'poster': poster,
        'genre': genre,
        'overview': overview,
        'cast': cast,
        'director': director
        })
    return render_template('base.html', movie_info = movie_info)

@app.route('/predict', methods=['POST'])
def predict():
    reply = chatbot.reply(request.json['message'])
    message = {'answer': reply}
    print('app.py 실행: ', message)
    return jsonify(message)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')
    print(search_query)
    search_results = movie_search.search_movies(search_query)
    print(search_results)
    return render_template('search.html', movie=search_results, search_query=search_query)

@app.route('/movie_data', methods=['GET'])
def movie_data():
    if 'movie_data' in session:
        return jsonify(session['movie_data'])
    else:
        return jsonify({'error': 'No movie data found in session'})

if __name__ == '__main__':
    app.run(debug=True)