import pandas as pd

path = "~/.cache/kagglehub/datasets/rounakbanik/the-movies-dataset/versions/7"

ratings = pd.read_csv(f"{path}/ratings.csv")
movies = pd.read_csv(f"{path}/movies_metadata.csv")

print (ratings.head())
print (movies.head())