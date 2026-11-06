
import pandas as pd
import ast

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

MOVIES_FILE = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_FILE = DATA_DIR / "tmdb_5000_credits.csv"

print("\n" + "=" * 50)
print("       🎬 CINEMATCH AI - INITIALIZATION")
print("=" * 50)


# ==========================================
# 2. LOAD DATASETS
# ==========================================

def load_datasets():

    if not MOVIES_FILE.exists():
        raise FileNotFoundError(
            f"Movies dataset not found: {MOVIES_FILE}"
        )

    if not CREDITS_FILE.exists():
        raise FileNotFoundError(
            f"Credits dataset not found: {CREDITS_FILE}"
        )

    movie_data = pd.read_csv(MOVIES_FILE)
    credit_data = pd.read_csv(CREDITS_FILE)

    print("✓ Movie dataset loaded")
    print("✓ Credits dataset loaded")

    return movie_data, credit_data


movies, credits = load_datasets()


# ==========================================
# 3. MERGE DATASETS
# ==========================================

credits = credits.rename(columns={
    "movie_id": "id",
    "title": "credits_title"
})

movies = movies.merge(
    credits,
    on="id",
    how="inner"
)

print("✓ Movie and credits datasets merged")


# ==========================================
# 4. SAFE DATA EXTRACTION
# ==========================================

def parse_data(value):
    """
    Safely convert string representations
    of Python lists into actual lists.
    """

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return [value]

    if pd.isna(value):
        return []

    try:

        result = ast.literal_eval(value)

        if isinstance(result, list):
            return result

        if isinstance(result, dict):
            return [result]

        return []

    except (ValueError, SyntaxError, TypeError):
        return []


# ==========================================
# 5. EXTRACT GENRES AND KEYWORDS
# ==========================================

def extract_names(value):
    """
    Extract genre and keyword names.
    """

    items = parse_data(value)

    return [
        str(item["name"]).strip()
        for item in items
        if isinstance(item, dict)
        and item.get("name")
    ]


# ==========================================
# 6. EXTRACT TOP CAST MEMBERS
# ==========================================

def extract_cast(value):
    """
    Extract the first three cast members.
    """

    items = parse_data(value)

    return [
        str(item["name"]).strip()
        for item in items[:3]
        if isinstance(item, dict)
        and item.get("name")
    ]


# ==========================================
# 7. EXTRACT DIRECTOR
# ==========================================

def extract_director(value):
    """
    Extract movie director names.
    """

    items = parse_data(value)

    return [
        str(item["name"]).strip()
        for item in items
        if isinstance(item, dict)
        and item.get("job") == "Director"
        and item.get("name")
    ]


# ==========================================
# 8. CLEAN AND PREPARE MOVIE DATA
# ==========================================

print("Processing movie features...")

movies["genres"] = movies["genres"].apply(extract_names)

movies["keywords"] = movies["keywords"].apply(extract_names)

movies["cast"] = movies["cast"].apply(extract_cast)

movies["crew"] = movies["crew"].apply(extract_director)

movies["overview"] = movies["overview"].fillna("").astype(str)

movies["title"] = movies["title"].fillna("").astype(str).str.strip()

# Remove empty movie titles

movies = movies[
    movies["title"].str.len() > 0
].copy()

# Remove duplicate movies

movies = movies.drop_duplicates(
    subset=["id"]
).copy()

movies.reset_index(drop=True, inplace=True)

print(f"✓ Processed {len(movies)} movies")


# ==========================================
# 9. CREATE MOVIE TAGS
# ==========================================

def create_tags(row):
    """
    Combine movie characteristics into
    a single text document.
    """

    overview = row["overview"]

    genres = " ".join(row["genres"])

    keywords = " ".join(row["keywords"])

    cast = " ".join(row["cast"])

    director = " ".join(row["crew"])

    tags = (
        overview + " " +
        genres + " " +
        genres + " " +
        keywords + " " +
        cast + " " +
        director + " " +
        director
    )

    return tags.lower()


movies["tags"] = movies.apply(
    create_tags,
    axis=1
)

# Keep only the required columns

movies = movies[
    [
        "id",
        "title",
        "genres",
        "overview",
        "tags"
    ]
].copy()

movies.reset_index(drop=True, inplace=True)

print("✓ Movie tags created successfully")


# ==========================================
# 10. TF-IDF VECTORIZATION
# ==========================================

print("Building TF-IDF model...")

tfidf = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True
)

vectors = tfidf.fit_transform(
    movies["tags"]
)

print("✓ TF-IDF vectorization completed")

print(f"✓ Feature matrix shape: {vectors.shape}")


# ==========================================
# 11. MOVIE RECOMMENDATION ENGINE
# ==========================================

def recommend_movies(movie_name, number_of_recommendations=5):
    """
    Recommend movies based on content similarity.

    Parameters:
        movie_name (str):
            Selected movie title.

        number_of_recommendations (int):
            Number of movies to recommend.

    Returns:
        list:
            Recommended movies with title,
            genres, overview and similarity.
    """

    # Validate movie name

    if not isinstance(movie_name, str) or not movie_name.strip():
        return []

    movie_name = movie_name.strip().casefold()

    # Validate recommendation count

    try:
        number_of_recommendations = int(
            number_of_recommendations
        )
    except (ValueError, TypeError):
        return []

    if number_of_recommendations <= 0:
        return []

    # Find selected movie

    matches = movies[
        movies["title"].str.casefold() == movie_name
    ]

    if matches.empty:
        return []

    movie_index = matches.index[0]

    # ======================================
    # CALCULATE SIMILARITY
    # ======================================

    selected_vector = vectors[movie_index]

    similarity_scores = linear_kernel(
        selected_vector,
        vectors
    ).flatten()

    # ======================================
    # SORT MOVIES BY SIMILARITY
    # ======================================

    sorted_indices = similarity_scores.argsort()[::-1]

    recommendations = []

    seen_titles = {movie_name}

    # ======================================
    # GENERATE RECOMMENDATIONS
    # ======================================

    for index in sorted_indices:

        # Skip selected movie

        if index == movie_index:
            continue

        movie = movies.iloc[index]

        title = movie["title"]

        # Avoid duplicate titles

        if title.casefold() in seen_titles:
            continue

        seen_titles.add(title.casefold())

        # Extract movie details

        overview = (
            movie["overview"]
            if movie["overview"]
            else "No description available."
        )

        genres = (
            ", ".join(movie["genres"])
            if movie["genres"]
            else "Genre unavailable"
        )

        similarity_percentage = round(
            float(similarity_scores[index]) * 100,
            2
        )

        recommendations.append({

            "title": title,

            "genres": genres,

            "overview": overview,

            "similarity": similarity_percentage

        })

        if len(recommendations) >= number_of_recommendations:
            break

    return recommendations


# ==========================================
# 12. SEARCH MOVIES
# ==========================================

def search_movies(query, limit=10):
    """
    Search movies by partial title.
    Useful for future search functionality.
    """

    if not isinstance(query, str) or not query.strip():
        return []

    query = query.strip().casefold()

    matches = movies[
        movies["title"].str.casefold().str.contains(
            query,
            regex=False
        )
    ]

    return matches["title"].head(limit).tolist()


# ==========================================
# 13. TERMINAL TEST
# ==========================================

if __name__ == "__main__":

    print("\n" + "=" * 50)

    print("       🎬 WELCOME TO CINEMATCH AI")

    print("=" * 50)

    print("\nDiscover movies similar to your favourites.\n")

    movie_name = input(
        "Enter your favourite movie: "
    )

    results = recommend_movies(
        movie_name,
        number_of_recommendations=5
    )

    if results:

        print(
            f"\n🍿 Movies similar to {movie_name}:\n"
        )

        for i, movie in enumerate(results, start=1):

            print(f"{i}. {movie['title']}")

            print(f"   Genre: {movie['genres']}")

            print(
                f"   Similarity: {movie['similarity']}%"
            )

            print(
                f"   Overview: {movie['overview'][:150]}..."
            )

            print("-" * 50)

    else:

        print("\n❌ No recommendations found.")

        suggestions = search_movies(movie_name)

        if suggestions:

            print("\nDid you mean:")

            for suggestion in suggestions[:5]:
                print(f" • {suggestion}")

        else:

            print(
                "Please check the movie title "
                "and try again."
            )

    print("\n🎬 Thank you for using CineMatch AI!")
