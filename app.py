from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the dataset
movie_data = pd.read_csv('mixed_movies_clean.csv')

# Fill missing values only for string columns
string_cols = movie_data.select_dtypes(include='object').columns
movie_data[string_cols] = movie_data[string_cols].fillna('')

# Prepare dropdown options
genre_list = sorted(set(genre.strip() 
                        for genres in movie_data['genre'].dropna() 
                        for genre in str(genres).split(',')))

industry_list = sorted(movie_data['industry'].dropna().unique())

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username 
        return redirect(url_for('home')) 
    return render_template('signup.html')

@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('index'))

    recommendations = []
    selected_genre = ''
    selected_industry = ''

    if request.method == 'POST':
        selected_genre = request.form['genre']
        selected_industry = request.form['industry']

        filtered = movie_data[
            movie_data['genre'].str.contains(rf'\b{selected_genre}\b', case=False, na=False) &
            (movie_data['industry'].str.lower() == selected_industry.lower())
        ]

        if not filtered.empty:
            recommendations = filtered.sample(n=min(5, len(filtered))).to_dict('records')

    return render_template('home.html',
                           username=session['username'],
                           genre_list=genre_list,
                           industry_list=industry_list,
                           selected_genre=selected_genre,
                           selected_industry=selected_industry,
                           recommendations=recommendations)

@app.route('/shuffle', methods=['POST'])
def shuffle():
    genre = request.form['genre']
    industry = request.form['industry']

    filtered = movie_data[
        movie_data['genre'].str.contains(rf'\b{genre}\b', case=False, na=False) &
        (movie_data['industry'].str.lower() == industry.lower())
    ]

    recommendations = []
    if not filtered.empty:
        recommendations = filtered.sample(n=min(5, len(filtered))).to_dict('records')

    return render_template('home.html',
                           username=session['username'],
                           genre_list=genre_list,
                           industry_list=industry_list,
                           selected_genre=genre,
                           selected_industry=industry,
                           recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
