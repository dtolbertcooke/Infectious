import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_name_from_game_id(game_id):
    return df[df.game_id == game_id]["name"].values[0]


def get_game_id_from_name(name):
    return df[df.name == name]["game_id"].values[0]


df = pd.read_csv("steam_games_dataset.csv")
# print(df.columns)

features = ['categories', 'genres', 'steamspy_tags', 'developer']

game_user_likes = "Left 4 Dead"


def combine_features(row):
    return row['categories'] + " " + row['genres'] + " " + row["steamspy_tags"] + " " + row["developer"]


df["combined_features"] = df.apply(combine_features, axis=1)

# print("Combined Features:", df["combined_features"].head())

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

cosine_sim = cosine_similarity(count_matrix)

game_index = get_game_id_from_name(game_user_likes)

similar_games = list(enumerate(cosine_sim[game_index]))
# print(similar_games)

sorted_similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)
# print(sorted_similar_games)

i = 0
for element in sorted_similar_games:
    print(get_name_from_game_id(element[0]))
    i = i + 1
    if i >= 6:
        break
