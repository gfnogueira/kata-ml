import pandas as pd
import argparse
import json
import os
import pickle
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

# Load configuration from JSON
CONFIG_FILE = "config.json"
DEFAULT_PATH = "~/.cache/kagglehub/datasets/rounakbanik/the-movies-dataset/versions/7"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    DATASET_PATH = config.get("dataset_path", DEFAULT_PATH)
else:
    DATASET_PATH = DEFAULT_PATH

print(f"Using dataset at: {DATASET_PATH}")

ratings_path = f"{DATASET_PATH}/ratings.csv"
movies_path = f"{DATASET_PATH}/movies_metadata.csv"
similarity_matrix_file = f"{DATASET_PATH}/similarity_matrix.pkl"

def create_ratings_sparse(file_path):
    # Creates a sparse rating matrix optimized for large datasets
    ratings = pd.read_csv(file_path, low_memory=False)
    ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors='coerce').fillna(0).astype(int)
    ratings['userId'] = ratings['userId'].astype('category').cat.codes
    ratings_sparse = csr_matrix((ratings['rating'], (ratings['userId'], ratings['movieId'])))
    
    return ratings_sparse, ratings

def compute_item_similarity_sparse(ratings_sparse):
    # Computes item similarity using a sparse matrix
    similarity_matrix = cosine_similarity(ratings_sparse.T, dense_output=False)
    
    return similarity_matrix

def get_movie_details(movie_id, movies_df):
    # Retrieves movie details, including genres, vote average, and vote count
    movie_info = movies_df[movies_df['movieId'] == movie_id]
    
    if movie_info.empty:
        return None
    
    genres = eval(movie_info.iloc[0]['genres']) if isinstance(movie_info.iloc[0]['genres'], str) else []
    genres = ", ".join([g['name'] for g in genres])
    vote_average = movie_info.iloc[0].get('vote_average', "N/A")
    vote_count = movie_info.iloc[0].get('vote_count', "N/A")
    
    return genres, vote_average, vote_count

def recommend_movies(movie_title, similarity_matrix, ratings_df, movies_df, top_n=10):
    # Returns the most similar movies to a given title, including genres, vote average, and vote count
    movies_df = movies_df.rename(columns={'id': 'movieId'})
    movies_df['movieId'] = pd.to_numeric(movies_df['movieId'], errors='coerce').fillna(0).astype(int)
    movie_entry = movies_df[movies_df['title'] == movie_title]
    
    if movie_entry.empty:
        return f"Movie '{movie_title}' not found."
    movie_id = int(movie_entry.iloc[0]['movieId'])
    
    if movie_id not in ratings_df['movieId'].unique():
        return f"Movie '{movie_title}' does not have enough ratings."
    
    movie_index = int(ratings_df[ratings_df['movieId'] == movie_id].iloc[0].movieId)
    sim_scores = similarity_matrix[movie_index].toarray().flatten()
    similar_indexes = sim_scores.argsort()[::-1][1:top_n+1]
    similar_movies = movies_df.iloc[similar_indexes]
    recommended_movies = []
    
    for _, row in similar_movies.iterrows():
        genres, vote_average, vote_count = get_movie_details(row['movieId'], movies_df)
        recommended_movies.append({
            "title": row['title'],
            "movieId": row['movieId'],
            "genres": genres,
            "vote_average": vote_average,
            "vote_count": vote_count
        })
        
    return pd.DataFrame(recommended_movies)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Item-Based Collaborative Filtering Recommendation")
    parser.add_argument("movie_title", type=str, help="Movie title for recommendation")
    parser.add_argument("--update", action='store_true', help="Force similarity matrix recalculation")
    args = parser.parse_args()
    
    print(f"Loading data for recommendation of '{args.movie_title}'...")
    
    ratings_sparse, ratings_df = create_ratings_sparse(ratings_path)
    movies_df = pd.read_csv(movies_path, low_memory=False)
    
    if args.update or not os.path.exists(similarity_matrix_file):
        
        print("Calculating movie similarity matrix...")
        
        similarity_matrix = compute_item_similarity_sparse(ratings_sparse)
        
        with open(similarity_matrix_file, "wb") as f:
            pickle.dump(similarity_matrix, f)
            
        print("Similarity matrix saved!")
        
    else:
        
        print("Loading saved similarity matrix...")
        
        with open(similarity_matrix_file, "rb") as f:
            similarity_matrix = pickle.load(f)
            
    recommended_movies = recommend_movies(args.movie_title, similarity_matrix, ratings_df, movies_df)
    
    print(f"Recommendations for '{args.movie_title}':")
    print(recommended_movies.to_string(index=False))
