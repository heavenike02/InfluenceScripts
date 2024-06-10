import csv
from collections import defaultdict
import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_lg")

def preprocess_text(text):
    """Preprocess text using spaCy."""
    # Convert to lowercase
    text = text.lower()
    # Remove template text
    template_texts = ["please describe your improvement request",
                      "what is the opportunity/problem the request will address?",
                      "what is the expected benefit?",
                      "tags general / others"
                      "sap analytics cloud"
                      "sac"]
    for template_text in template_texts:
        text = text.replace(template_text.lower(), "")
    # Tokenize and preprocess the remaining text using spaCy
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]  # Remove punctuation and stop words
    return " ".join(tokens)

def compare_text(text1, text2):
    """Compare two texts using spaCy similarity."""
    # Preprocess both texts
    doc1 = preprocess_text(text1)
    doc2 = preprocess_text(text2)
    # Calculate the similarity score between the two preprocessed texts
    similarity_score = nlp(doc1).similarity(nlp(doc2))
    return similarity_score

# Read the CSV file and extract the influence coach names and descriptions
csv_file = r"C:\Users\I586445\Downloads\Influence tickets.csv"  # Replace 'data.csv' with your CSV file path
influence_data = defaultdict(list)
processed_ids = set()  # Set to track processed influence IDs

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    # Iterate through each row in the CSV file
    for row in reader:
        influence_id = row[0]  # Update with the index of influence ID
        influence_coach = row[4]  # Update with the index of influence coach
        description = row[16]  # Update with the index of description
        
        # Ensure that description is not empty
        if description.strip():
            # Store the influence coach name and description along with the corresponding influence ID
            influence_data[influence_id].append((influence_coach, description))

# Create a new CSV file to store the result
output_file = 'result.csv'  # Name of the new CSV file
fieldnames = ['influence_id', 'influence_coach', 'level_of_similarity']

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each influence ID and its associated coach names and descriptions
    for influence_id, coach_descriptions in influence_data.items():
        if influence_id in processed_ids:
            continue  # Skip processing if influence ID has already been processed

        print(f"Processing Influence ID: {influence_id}")

        for coach, description in coach_descriptions:
            print(f"Comparing Influence ID: {influence_id} - Coach: {coach}")

            # Compare each description with all other descriptions to find the most similar one
            for other_influence_id, other_descriptions in influence_data.items():
                if other_influence_id == influence_id or other_influence_id in processed_ids:
                    continue  # Skip if comparing with itself or with already processed ID

                for other_coach, other_description in other_descriptions:
                    similarity_score = compare_text(description, other_description)
                    print(f"Issue {influence_id} compared to {other_influence_id} equals {similarity_score}")
                    if similarity_score > 0.95:
                        print(f"GREATER Issue {influence_id} compared to {other_influence_id} equals {similarity_score}")

        # Mark the current influence ID as processed
        processed_ids.add(influence_id)

        # Write the result to the new CSV file
        writer.writerow({
            'influence_id': influence_id,
            'influence_coach': coach,
            'level_of_similarity': similarity_score
        })

print("Result saved to result.csv")
