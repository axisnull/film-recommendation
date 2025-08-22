import json
import pickle
from tmdbv3api import Movie, TMDb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googletrans import Translator


movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'cf90de25f653998506d6c07e69090a54'
tmdb.language = 'ko-KR'

movies = pickle.load(open('cosine/movies.pkl', 'rb'))

#영화 정보 데이터 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies['soup'])

class MovieSearcher():
    def __init__(self) -> None:
        pass

    def random_movies(self):
        rd_movie = movies.sample(4)
        return rd_movie.to_json(orient='records')

    def search(self):
        movie_list = self.random_movies()
        idx = [movie['id'] for movie in json.loads(movie_list)]
        print(idx)
        titles = []
        posters = []
        genres = []
        overviews = []
        cast = []
        director = []
        for i in idx:
            details = movie.details(i)
            #print(details)
            image_path = details['poster_path']
            image_path = 'https://image.tmdb.org/t/p/w500/' + image_path

            titles.append(details['title'])
            posters.append('https://image.tmdb.org/t/p/w500/' + image_path)
            genres_list = [genre['name'] for genre in details['genres']]
            genres.append(', '.join(genres_list))
            overviews.append(details['overview'])
            cast_list = [person['name'] for person in details['casts']['cast'] if person['known_for_department'] == 'Acting']
            cast.append(', '.join(cast_list[:5]))
            director_list = [person['name'] for person in details['casts']['crew'] if person['job'] == 'Director']
            director.append(', '.join(director_list[:1]))
            
        #return titles, posters, json.loads(movie_list)
        return titles, posters, genres, overviews, cast, director

    def search_movies(self, query):
        search_results = movie.search(query)
        search_movie = search_results[0].id
        search_movie = movie.details(search_movie)
        #print(search_movie.title)
        #print(search_movie.overview)
        poster = []
        genres = []
        cast = []
        director = []
        poster.append('https://image.tmdb.org/t/p/w500/' + search_movie.poster_path)
        #print(poster)
        genres_list = [genre['name'] for genre in search_movie['genres']]
        genres.append(', '.join(genres_list))
        cast_list = [person['name'] for person in search_movie['casts']['cast'] if person['known_for_department'] == 'Acting']
        cast.append(', '.join(cast_list[:5]))
        director_list = [person['name'] for person in search_movie['casts']['crew'] if person['job'] == 'Director']
        director.append(', '.join(director_list[:1]))  
        movie_result = {
            'title': search_movie.title,
            'poster': poster,
            'genres': genres,
            'overview': search_movie.overview,
            'cast': cast,
            'director': director
        }
        return movie_result

#titles, posters, genres, overviews, cast, director = MovieSearcher().search()
#print(titles)
#print(posters)
#print(genres)
#print(overviews)
#print(cast)
#print(director)

#search_movie = MovieSearcher().search_movies('기생충')
#print(search_movie)

#moviesearch = MovieSearcher()
#df = moviesearch.search_movies('Up')
#print(df[0]['genres'])

class CosineSimilarity():
    def __init__(self) -> None:
        pass

    def translate_to_english(self, text):
        translator = Translator()
        translated_text = translator.translate(text, dest='en').text
        return translated_text

    def combine_proper_nouns(self, text):
        combined_text = re.sub(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', lambda m: m.group(0).replace(' ', ''), text)
        return combined_text

    def preprocess(self, text):
        tokens = []
        if isinstance(text, list):
            text = ''.join(text)
        text = self.translate_to_english(text)
        text = self.combine_proper_nouns(text)
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        user_token = word_tokenize(text)
        for word in user_token:
            if word not in stopwords.words('english'):
                tokens.append(word)
        return ' '.join(tokens)

    # 추천 영화 타이틀, 포스터
    def recommend(self, input_vector, tfidf_matrix):
        cosine_sim = cosine_similarity(input_vector, tfidf_matrix)
        similarity_scores = cosine_sim.flatten()
        recommended_movie_indices = similarity_scores.argsort()[-5:-1][::-1]

        titles = []
        posters = []
        for idx in recommended_movie_indices:
            movie_id = movies.iloc[idx]['id']
            #print(movie_id)
            details = movie.details(movie_id)

            image_path = details['poster_path']

            titles.append(details['title'])
            posters.append('https://image.tmdb.org/t/p/w500/' + image_path)
            #posters.append(image_path)
        return titles, posters

    def result(self, user_input):
        # 사용자 입력 토큰화
        #translated_input = self.translate_to_english(user_input)
        #processed_input = self.preprocess(translated_input)
        input_vector = vectorizer.transform([user_input])
        print('cosine.py user input: '+user_input)

        # 코사인 유사도로 영화 추천
        titles, posters = self.recommend(input_vector, tfidf_matrix)
        print(titles)
        return titles, posters

# 사용자 입력
#user_input = "hi sf action thriller enjoyed interstellar leonardodicaprio likes handsome"
#CosineSimilarity().result(user_input)