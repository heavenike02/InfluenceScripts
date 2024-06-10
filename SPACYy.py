import spacy
import csv
from collections import defaultdict

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Preprocess text using spaCy."""
    # Tokenize and preprocess the text using spaCy
    doc = nlp(text)
    return doc

def compare_text(text1, text2):
    """Compare two texts using spaCy similarity."""
    # Preprocess both texts
    doc1 = preprocess_text(text1)
    doc2 = preprocess_text(text2)
    # Calculate the similarity score between the two preprocessed texts
    similarity_score = doc1.similarity(doc2)
    return similarity_score

# Read the CSV file and extract the influence coach names and descriptions
csv_file = r"C:\Users\I586445\Downloads\model refresh\SAP Analytics Cloud & SAP Digital Boardroom.csv"  # Replace 'data.csv' with your CSV file path
influence_data = defaultdict(list)

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    # Iterate through each row in the CSV file
    for row in reader:
        influence_id = row['influence_id']
        influence_coach = row['influence_coach']
        description = row['description']
        # Store the influence coach name and description along with the corresponding influence ID
        influence_data[influence_id].append((influence_coach, description))

# Create a new CSV file to store the result
output_file = 'result.csv'  # Name of the new CSV file
fieldnames = ['influence_id', 'influence_coach', 'most_similar_id', 'level_of_similarity', 'most_similar_description']

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each influence ID and its associated coach names and descriptions
    for influence_id, coach_descriptions in influence_data.items():
        max_similarity = 0
        most_similar_id = None
        most_similar_description = None

        for coach, description in coach_descriptions:
            # Compare each description with all other descriptions to find the most similar one
            for other_coach, other_description in coach_descriptions:
                if coach != other_coach:  # Avoid comparing with itself
                    similarity_score = compare_text(description, other_description)
                    if similarity_score > max_similarity:
                        max_similarity = similarity_score
                        most_similar_id = influence_id
                        most_similar_description = other_description

        # Write the result to the new CSV file
        writer.writerow({
            'influence_id': influence_id,
            'influence_coach': coach,
            'most_similar_id': most_similar_id,
            'level_of_similarity': max_similarity,
            'most_similar_description': most_similar_description
        })

print("Result saved to 'result.csv'")
