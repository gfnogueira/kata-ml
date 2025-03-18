# **Item-Based Collaborative Filtering Recommendation System**

This project implements an **Item-Based Collaborative Filtering** recommendation system, which suggests movies similar to a given movie based on user ratings.

## **📌 Project Structure**
The system consists of several key scripts:

| File | Description |
|-------------------------|---------------------------------------------------------------|
| `download.py` | Downloads the dataset from Kaggle and stores it in a local directory. |
| `item_based_filtering.py` | Main script that loads ratings, calculates similarity, and recommends movies. |
| `config.json` | Stores the dataset path to avoid hardcoding it inside scripts. |
| `requirements.txt` | Lists the required Python dependencies. |

## **🚀 How to Install and Run**

### **1️⃣ Set Up a Virtual Environment**
It is recommended to run the project in a virtual environment to isolate dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

### **2️⃣ Install Dependencies**
Make sure you have Python installed and then install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```
The `requirements.txt` includes:
```
kagglehub
pandas
ipython
scikit-learn
```

### **3️⃣ Download the Dataset**
Before running the recommendation system, you need to download the dataset. Run:
```bash
python download.py
```
This will fetch the dataset from Kaggle and store it in:
```
~/.cache/kagglehub/datasets/rounakbanik/the-movies-dataset/versions/7
```
If you prefer to move the dataset to another location, you can do so and then update the path in **`config.json`**.

### **4️⃣ Configure the Dataset Path**
If the dataset is stored in a different location, edit `config.json` and set the correct path:
```json
{
    "dataset_path": "~/.cache/kagglehub/datasets/rounakbanik/the-movies-dataset/versions/7"
}
```
This ensures the system knows where to find the required CSV files.

### **5️⃣ Run the Movie Recommendation System**
To get movie recommendations for a given title, run:
```bash
python item_based_filtering.py "The Godfather"
```
📌 The output will display **similar movies** along with their **genres, average rating, and vote count**.

### **6️⃣ Update the Similarity Matrix (Only When Needed)**
The similarity matrix is cached to **avoid recalculating it every time**, which speeds up execution. However, if you update the dataset or want to recompute the similarity matrix, run:
```bash
python item_based_filtering.py "The Godfather" --update
```
This **recomputes and saves the similarity matrix**, preventing redundant recalculations in future runs.

## **📌 Understanding the Output**
The output displays the **top similar movies** based on user ratings.

Example:
```
Recommendations for 'The Godfather':
             title  movieId                                              genres  vote_average  vote_count
           Amateur    30157                      Crime, Comedy, Drama, Thriller           6.5        21.0
   Made in America    12121                                              Comedy           5.3        86.0
      Sudden Death     9091                         Action, Adventure, Thriller           5.5       174.0
    Miami Rhapsody    17402                                     Comedy, Romance           5.6         7.0
Heavenly Creatures     1024                                      Drama, Fantasy           6.9       299.0
 A Little Princess    19101                              Drama, Family, Fantasy           7.4       207.0
   Johnny Mnemonic     9886 Adventure, Action, Drama, Science Fiction, Thriller           5.5       380.0
           Georgia    97406                                               Drama           6.1        15.0
    Body Snatchers     4722                   Horror, Science Fiction, Thriller           5.8       102.0
The Little Rascals    10897                             Romance, Comedy, Family           6.3       214.0
```

### **Explanation of Columns**
- **`title`** → Name of the recommended movie.
- **`movieId`** → Unique ID of the movie.
- **`genres`** → Genres associated with the movie.
- **`vote_average`** → Average user rating from the dataset.
- **`vote_count`** → Number of votes the movie has received.

---

## **📌 Notes**
- The system **uses user ratings** to compare movies, meaning the recommendations are **collaborative-based, not content-based**.
- It **does NOT require user input preferences**, as it analyzes collective ratings.
- If the dataset is updated, use `--update` to **recompute the similarity matrix**.

