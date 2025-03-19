import kagglehub
import os
import shutil
import pandas as pd


DATASET_DIR = "data/the-movies-dataset"


DEFAULT_DOWNLOAD_PATH = kagglehub.dataset_download("rounakbanik/the-movies-dataset")


if not os.path.exists(DATASET_DIR):
    print(f"Movendo dataset para {DATASET_DIR}...")
    shutil.move(DEFAULT_DOWNLOAD_PATH, DATASET_DIR)
else:
    print("Dataset já está na pasta correta.")


path = f"{DATASET_DIR}/kagglehub/datasets/rounakbanik/the-movies-dataset/versions/7"


ratings_file = os.path.join(path, "ratings.csv")
movies_file = os.path.join(path, "movies_metadata.csv")

if os.path.exists(ratings_file) and os.path.exists(movies_file):
    ratings = pd.read_csv(ratings_file)
    movies = pd.read_csv(movies_file)
    print("Dados carregados com sucesso!")
    print(ratings.head())
    print(movies.head())
else:
    print("Arquivos CSV não encontrados!")