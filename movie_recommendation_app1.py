import pandas
import sklearn.feature_extraction.text
import sklearn.metrics.pairwise
import tmdbv3api
import streamlit

credits_data = pandas.read_csv("tmdb_5000_credits.csv")
movies_data = pandas.read_csv("tmdb_5000_movies.csv")

credits_data.columns = ["id", "title", "cast", "crew"]

data = movies_data.merge(credits_data[["id", "cast", "crew"]], on = "id")

####################################################################################################

# Movie Recommendation based on overview(main plot points, storyline, etc.)

tfidf = sklearn.feature_extraction.text.TfidfVectorizer(stop_words = "english")
data["overview"] = data["overview"].fillna("")
tfidf_matrix = tfidf.fit_transform(data["overview"])

cosine_similarity1 = sklearn.metrics.pairwise.linear_kernel(tfidf_matrix, tfidf_matrix)

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
            image_path = "no_image.jpg"

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

# To run the program and open the web page, enter "streamlit run movie_recommendation_app1.py" as input in terminal