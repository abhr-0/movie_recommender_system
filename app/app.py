import streamlit as st
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

movies_dict = pickle.load(open("app/movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("app/similarity.pkl", "rb"))

st.title("Movie Recommender System")

selected = st.selectbox("Enter movie name:", movies["title"].values)

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}")
    data = response.json()
    # st.text(data)
    return "https://images.tmdb.org/t/p/w500" + data["poster_path"]

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

if st.button("Recommend"):
    recommendations, posters = recommend(selected)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(recommendations[0])
    with col2:
        st.image(posters[1])
        st.text(recommendations[1])
    with col3:
        st.image(posters[2])
        st.text(recommendations[2])
    with col4:
        st.image(posters[3])
        st.text(recommendations[3])
    with col5:
        st.image(posters[4])
        st.text(recommendations[4])