import supabase
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import ast
import os
from dotenv import load_dotenv
# Assuming 'model' is already defined and loaded elsewhere in your script

# Load environment variables
load_dotenv()

# Replace with your Supabase connection details
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

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

# Get user input for semantic search
user_query = input("Enter your search phrase: ")

# Embed the user query
query_vector = model.encode(user_query)
query_vector = np.array(query_vector).reshape(1, -1)  # Reshape for cosine_similarity

# Perform semantic search
similarity_scores = cosine_similarity(query_vector, vectors)
sorted_indices = np.argsort(similarity_scores[0])[::-1]  # Sort indices by score, descending

# Prepare results
results = [{'id': ids[i], 'score': similarity_scores[0][i]} for i in sorted_indices]

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save to CSV, filename based on user input
csv_filename = f"semantic_search_{user_query}.csv".replace(" ", "_")
results_df.to_csv(csv_filename, index=False)

print(f"Results saved to {csv_filename}")