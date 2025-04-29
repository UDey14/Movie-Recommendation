from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load the movie dataset
movies = pd.read_csv('mixed_movies_clean.csv')

# Create a TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Fill missing overviews with empty string
movies['overview'] = movies['overview'].fillna('')

# Fit the model
tfidf_matrix = tfidf.fit_transform(movies['overview'])

# Compute similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def get_recommendations(genre, industry):
    filtered_movies = movies[
        (movies['genre'].str.lower() == genre.lower()) &
        (movies['industry'].str.lower() == industry.lower())
    ]

    if filtered_movies.empty:
        return []

    idx = filtered_movies.index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar movies

    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices][['title']].to_dict(orient='records')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Recommend route
@app.route('/recommend')
def recommend():
    genre = request.args.get('genre')
    industry = request.args.get('industry')
    if not genre or not industry:
        return jsonify({"error": "Missing genre or industry"}), 400

    recommendations = get_recommendations(genre, industry)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
