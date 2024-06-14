import supabase
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import ast
import os 
from dotenv import load_dotenv
# Replace with your Supabase connection details
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Define the Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
print("Connected to Supabase")

# Fetch all data from Supabase in one call
try:
    response = supabase_client.table('new').select('id', 'vec').execute()
    data = response.data
    print(f"Fetched {len(data)} rows from Supabase")
except Exception as e:
    print(f"Error fetching data from Supabase: {e}")
    exit()

# Extract vectors and IDs
ids = [item['id'] for item in data]
vectors = [item['vec'] for item in data]

# Convert vectors from strings to lists of floats
try:
    vectors = [ast.literal_eval(vec) for vec in vectors]
    print("Vectors converted from strings to lists")
except Exception as e:
    print(f"Error converting vectors from strings to lists: {e}")

# Convert vectors to numpy array
try:
    vectors = np.array(vectors, dtype=float)
    print("Vectors converted to numpy array")
except Exception as e:
    print(f"Error converting vectors to numpy array: {e}")

# Calculate cosine similarity matrix
try:
    similarity_matrix = cosine_similarity(vectors)
    print("Cosine similarity matrix calculated")
except Exception as e:
    print(f"Error calculating cosine similarity: {e}")

# Minimum similarity threshold (in percentage)
MIN_SIMILARITY_THRESHOLD = 70

# Prepare the data for CSV with similarity percentages and apply threshold
csv_data = []
for idx, feature_id in enumerate(ids):
    similarity_scores = similarity_matrix[idx]
    top_indices = similarity_scores.argsort()[-6:-1][::-1]  # Exclude self and get top 5
    for i in top_indices:
        similarity_percentage = (similarity_scores[i] + 1) / 2 * 100
        if similarity_percentage >= MIN_SIMILARITY_THRESHOLD:
            csv_data.append({
                'Feature ID': feature_id,
                'Similar Feature ID': ids[i],
                'Similarity Percentage': similarity_percentage
            })
    print(f"Top similar features for feature ID {feature_id} found and filtered by similarity threshold")

# Create DataFrame and save to CSV
df = pd.DataFrame(csv_data)
df.to_csv('full_similar_product_features.csv', index=False)
print("CSV file 'full_similar_product_features.csv' created successfully")
