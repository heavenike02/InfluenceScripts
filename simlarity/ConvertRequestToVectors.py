import csv
from sentence_transformers import SentenceTransformer
import vecs
from flupy import flu
from tqdm import tqdm
from typing import List, Tuple, Dict
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv()

# Load the database connection string from the environment variables
DB_CONNECTION = os.getenv("DB_CONNECTION")

# Create vector store client
vx = vecs.create_client(DB_CONNECTION)
print("Connected to vector store")

# Create a PostgreSQL/pgvector table named "product_requests" to contain the request embeddings
product_requests = vx.get_or_create_collection(name="product_requests", dimension=384)

# Load the CSV file
csv_file = r"C:\Users\I586445\Downloads\improvement request_12-06-2024_11-48\SAP Analytics Cloud & SAP Digital Boardroom.csv"

def preprocess_description(description: str) -> str:
    # Sentences to exclude
    sentences_to_exclude = [
        "Please describe your improvement request",
        "What is the opportunity/problem the request will address?",
        "What is the expected benefit?"
    ]

    # Remove the sentences
    for sentence in sentences_to_exclude:
        description = description.replace(sentence, "").strip()
    return description
# Read the CSV file and extract the product feature requests
requests = []
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for row in reader:
        request_id = row[0]  # Assuming the request id is in the first column
        description = row[16]  # Assuming the description is in the second column
        requests.append((request_id, description))

# Initialize the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

batch_size = 50
records: List[Tuple[str, np.ndarray, Dict]] = []

# Process the dataset in chunks
for chunk_ix, chunk in tqdm(enumerate(flu(requests).chunk(batch_size)), desc="Processing chunks"):
    # Extract just the descriptions from the current chunk
    chunk_descriptions = [preprocess_description(description) for _, description in chunk]
    # Create embeddings for the current chunk
    embedding_chunk = model.encode(chunk_descriptions)

    # Enumerate the embeddings and create a record to insert into the database
    for row_ix, embedding in enumerate(embedding_chunk):
        actual_request_id = chunk[row_ix][0]  # Get the actual request_id from the chunk
        records.append((actual_request_id, embedding, {"text": chunk_descriptions[row_ix]}))

# Insert the records into the collection
for record in tqdm(records, desc="Inserting records"):
    product_requests.upsert([record])

print("All product feature requests have been embedded and inserted into the collection.")

product_requests.create_index()
