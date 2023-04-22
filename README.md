# Movie_Recommendation_System_Using_Python
An application that allows users to enter into their account, choose their favourite movie, and then find comparable movies to that movie.

<img width="1440" alt="Screenshot 2023-04-22 at 3 37 35 PM" src="https://user-images.githubusercontent.com/106465081/233777857-a2d67d2f-f861-4e69-af75-af3ce30cc4a4.png">

# Recommendation System
A recommendation engine is a sort of machine learning that gives relevant suggestions to clients. Prior to the recommendation system, the most prevalent method of purchasing was to ask friends for suggestions. However, Google now knows what news you will read based on your search history, watch history, and purchase history, and YouTube knows what sort of videos you will watch based on your search history, watch history, and purchase history. A recommendation system assists a company in attracting loyal customers and developing trust by offering them with the products and services for which they visit your website. Today's recommendation algorithms are so advanced that they can handle even first-time visitors to the site. They can also suggest items that are currently popular or highly rated. For this project I used content-based filtering.
# Content-Based Filtering
The system recommends a product that is similar to those previously seen. To put it another way, with this algorithm, we're looking for objects that appear to be similar. If you like Sachin Tendulkar's shots, you might also like Ricky Ponting's shots because the two videos have similar tags and categories. Only the material looks to be the same, and there is no additional attention from the spectator. Based on past choices, only the product with the highest score is recommended.
# Dataset
The dataset was obtained from Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv It consists of two CSV files, one containing movie data and the other including credits for that movie.
# Tech Stack
- Python
- Pandas
- Streamlit
- NLTK
- Pickle
- Requests
# Data Collection
➤ Kaggle provided the data, which is based on the "TMDB 5000" Movie Dataset.
# Data Processing
➤ The dataset will be cleaned of any missing or duplicate values.
# Feature Selection
➤ We will not use all of the feature columns. We will only choose those who we feel will help us make suggestions.
# Feature extractions:
➤ We'll employ tags extracted from some of the specified features in our recommendation system.
# Stemming
➤ Porter stemming is a method for performing stemming operations on the column of a tag. The NLTK library in Python is used for this.
Stemming is the process of reducing a word to its word stem, which affixes to suffixes and prefixes or to the roots of words known as lemma. For example, a stemming algorithm changes the words "chocolates," "chocolatey," and "choco" to the root word "chocolate," and "retrieval," "retrieved," and "retrieves" to the stem "retrieve."
# Creating Vectors
➤ Using cosine similarity, I have constructed vectors for relevant movies based on the tags column and then measured the cosine distance. The cosine similarity measure is used to determine how similar papers are, regardless of size. It computes the cosine of the angle created by two three-dimensionally projected vectors. Because of the cosine similarity, even if two equivalent sentences are separated by the Euclidean distance (due to document size), they are likely to be oriented closer together. The lower the angle, the greater the cosine similarity.
# Recommendations:
➤ We propose the five films for the corresponding selected movie based on the top five nearest vectors by cosine similarity.
