# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template

from sklearn.linear_model import LogisticRegression # for example

from web_app.models import User, Tweet
from web_app.services.basilica_service import connection as basilica_connection

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
    # todo: wrap in a try block in case the user's don't exist in the database

    # f"SELECT * FROM users WHERE screen_name = {screen_name_a}"

    user_a = User.query.filter_by(screen_name = screen_name_a).one()
    user_b = User.query.filter_by(screen_name = screen_name_b).one()
    user_a_tweets = user_a.tweets # Tweet.query.filter_by(user_id = user_a.id).one()
    user_b_tweets = user_b.tweets # Tweet.query.filter_by(user_id = user_b.id).one()
    #user_a_embeddings = [tweet.embedding for tweet in user_a_tweets]
    #user_b_embeddings = [tweet.embedding for tweet in user_b_tweets]
    print("USER A", user_a.screen_name, len(user_a.tweets))
    print("USER B", user_b.screen_name, len(user_b.tweets))

    print("-----------------")
    print("TRAINING THE MODEL...")
    embeddings = []
    labels = []

    for tweet in user_a_tweets:
        embeddings.append(tweet.embedding)
        labels.append(user_a.screen_name)

    for tweet in user_b_tweets:
        embeddings.append(tweet.embedding)
        labels.append(user_b.screen_name)

    classifier = LogisticRegression() # for example
    classifier.fit(embeddings, labels)

    print("-----------------")
    print("MAKING A PREDICTION...")
    #result_a = classifier.predict([user_a_tweets[0].embedding])
    #result_b = classifier.predict([user_b_tweets[0].embedding])
    #results = classifier.predict([embeddings[0]])[0] #> elon

    example_embedding = basilica_connection.embed_sentence(tweet_text, model="twitter")
    result = classifier.predict([example_embedding])

    return render_template("prediction_results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely= result[0]
    )