import pandas
import numpy
import sklearn.feature_extraction.text
import sklearn.metrics.pairwise
import ast
import tmdbv3api
import streamlit

credits_data = pandas.read_csv("./data/tmdb_5000_credits.csv")
movies_data = pandas.read_csv("./data/tmdb_5000_movies.csv")

credits_data.columns = ["id", "title", "cast", "crew"]

data = movies_data.merge(credits_data[["id", "cast", "crew"]], on = "id")

####################################################################################################

# Movie Recommendation based on cast, director, genres and keywords

features1 = ["cast", "crew", "genres", "keywords"]
for feature in features1:
    data[feature] = data[feature].apply(ast.literal_eval)

def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return numpy.nan

data["director"] = data["crew"].apply(get_director)

def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

features2 = ["cast", "genres", "keywords"]
for feature in features2:
    data[feature] = data[feature].apply(get_list)

def adjust_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ""

features3 = ["cast", "director", "genres", "keywords"]
for feature in features3:
    data[feature] = data[feature].apply(adjust_data)

def concatenate_data(x):
    cast = " ".join(x["cast"])
    director = x["director"]
    genres = " ".join(x["genres"])
    keywords = " ".join(x["keywords"])
    return cast + " " + director + " " + genres + " " + keywords

data["concatenated_data"] = data.apply(concatenate_data, axis = 1)

count = sklearn.feature_extraction.text.CountVectorizer(stop_words = "english")
count_matrix = count.fit_transform(data["concatenated_data"])

cosine_similarity1 = sklearn.metrics.pairwise.cosine_similarity(count_matrix, count_matrix)

####################################################################################################

data = data.reset_index()
movies = data[["id", "title"]].copy()

movie = tmdbv3api.Movie()
tmdb = tmdbv3api.TMDb()

tmdb.api_key = "a9a70d6e2834d25889ca3465084e5765"

def get_recommendations(title):
    index = movies[movies["title"] == title].index[0]

    cosine_similarity_scores = list(enumerate(cosine_similarity1[index]))
    cosine_similarity_scores = sorted(cosine_similarity_scores, key = lambda x: x[1], reverse = True)
    cosine_similarity_scores = cosine_similarity_scores[1:26]

    movie_indices = [i[0] for i in cosine_similarity_scores]
    images = []
    titles = []

    for i in movie_indices:
        id = movies["id"].iloc[i]
        details = movie.details(id)
        image_path = details["poster_path"]

        if image_path:
            image_path = "https://image.tmdb.org/t/p/w500" + image_path
        else:
            image_path = "./image/no_image.jpg"

        images.append(image_path)
        titles.append(details["title"])
    return images, titles

streamlit.set_page_config(layout = "wide")
streamlit.header("Movie Recommendation based on cast, director, genres and keywords")

movie_list = movies["title"].values
title = streamlit.selectbox("Choose a movie you like", movie_list)

if streamlit.button("Get Recommendations"):
    with streamlit.spinner("Loading..."):
        images, titles = get_recommendations(title)
        index = 0
        for _ in range(5):
            cols = streamlit.columns(5)
            for col in cols:
                col.image(images[index])
                col.write(titles[index])
                index += 1