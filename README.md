# 🎬 CineMatch AI – Movie Recommendation System

An AI-powered movie recommendation system that suggests similar movies based on their genres, keywords, cast, director, and plot descriptions.

Built using Python, Machine Learning, and Streamlit as part of my **30 Days 30 AI Projects Challenge – Day 06**.

## ✨ Features

- Search and select movies from the TMDB 5000 dataset.
- Get 5 similar movie recommendations.
- Content-based recommendation engine.
- TF-IDF text vectorization.
- Cosine similarity calculation.
- Interactive Streamlit web application.
- Displays movie genres, descriptions, and similarity scores.

## 🧠 How It Works

CineMatch AI uses Content-Based Filtering.

1. Loads movie information and credits datasets.
2. Extracts genres, keywords, top cast members, and directors.
3. Combines these features with movie descriptions to create movie tags.
4. Converts text into numerical vectors using TF-IDF.
5. Calculates similarity between movies using Cosine Similarity.
6. Recommends the five most similar movies.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- Streamlit

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/21vicky/CineMatch-AI.git
```

### 2. Navigate to the project folder

```bash
cd CineMatch-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

## 📊 Machine Learning Concepts

| Concept | Purpose |
|---|---|
| Content-Based Filtering | Recommends movies using their content |
| TF-IDF | Converts text into numerical features |
| Cosine Similarity | Measures similarity between movie vectors |
| Feature Extraction | Extracts useful movie information |

## 📁 Dataset

This project uses the TMDB 5000 Movie Dataset.

Dataset source: [Kaggle – TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

Download both CSV files and place them inside the `data/` directory.

## 🚀 Future Improvements

- Movie poster integration.
- User ratings and personalized recommendations.
- Improved recommendation algorithms.
- Movie search and filtering enhancements.
- Cloud deployment.

## 👨‍💻 Author

**Vignesh U**

GitHub: [@21vicky](https://github.com/21vicky)

---

⭐ If you find this project interesting, consider giving it a star!

**30 Days 30 AI Projects – Day 06 | Keep Learning. Keep Building.**