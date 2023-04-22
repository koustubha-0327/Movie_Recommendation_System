import streamlit as st
import pandas as pd
import requests
import sqlite3
import pickle
# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib
from PIL import Image


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management


conn = sqlite3.connect('data.db')
c = conn.cursor()


# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users_table(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO users_table(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM users_table WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM users_table')
    data = c.fetchall()
    return data


def main():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # homepage configuration
    st.set_page_config(page_title="Flicks & Chill", page_icon=":tada:", layout="wide")
    st.title("Flicks & Chill: Your Movie Must-Sees 📽️🎞️🎧")
    st.text("Find the best movies you want to watch")



    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    # sidebar for Login/Signup

    if choice == "Home":
        st.subheader("Home")
        st.write("##")
        st.write(
            '''
            WELCOME TO Flicks & Chill.
            - Pick a Flick and Get Recommendations for Similar Movies to Enjoy !!
            '''
        )
        image = Image.open('bg_image.png')
        st.image(image, caption=None)

    # for login section
    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))

            if result:

                st.success("Logged In as {}".format(username))

                if username == "admin" and password == "admin@123":
                    task = st.selectbox("Task", ["Movie_list", "Profiles", "Movie_Profiles"])
                else:
                    task = st.selectbox("Task", ["Movie_list", "Movie_Profiles"])

                if task == "Movie_list":
                    st.subheader("List goes here")
                    for i in range(len(movies['title'].values)):
                        st.text(movies['title'].values[i])

                elif username == "admin" and password == "admin@123" and task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    st.dataframe(clean_db)
                    st.balloons()

                elif task == "Movie_Profiles":
                    st.subheader(" Movies")

                    # Poster path Key reference collected to fetch poster.
                    # Movie Poster will be returned when fetch_poster is called.
                    def fetch_poster(movie_id):
                        response = requests.get(
                            'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
                                movie_id))
                        data = response.json()
                        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

                    # selecting movie_id as a reference from movies for recommending .
                    # finding similarity distance for selected movie_index.
                    # based on sorted similarity distances top 5 relevant movies are stored into a list.
                    # from this list movies are returned by function call.

                    def recommend(movie):
                        movie_index = movies[movies['title'] == movie].index[0]
                        distances = similarity[movie_index]
                        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
                        recommended_movies = []
                        recommend_movies_posters = []
                        for i in movies_list:
                            movie_id = movies.iloc[i[0]].movie_id
                            recommended_movies.append(movies.iloc[i[0]].title)
                            recommend_movies_posters.append(fetch_poster(movie_id))
                        return recommended_movies, recommend_movies_posters

                    selected_movie_name = st.selectbox("Pick a movie you want", movies['title'].values)

                    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

                    # Displaying movie names and posters

                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.text(recommended_movie_names[0])
                        st.image(recommended_movie_posters[0])
                    with col2:
                        st.text(recommended_movie_names[1])
                        st.image(recommended_movie_posters[1])

                    with col3:
                        st.text(recommended_movie_names[2])
                        st.image(recommended_movie_posters[2])
                    with col4:
                        st.text(recommended_movie_names[3])
                        st.image(recommended_movie_posters[3])
                    with col5:
                        st.text(recommended_movie_names[4])
                        st.image(recommended_movie_posters[4])
                    st.snow()
                    st.snow()

        else:
            st.warning("please login")

    # Sign up -creating account with username and password

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
