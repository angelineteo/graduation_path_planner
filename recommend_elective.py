import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_path = 'formatted_refined_table.csv'
# Create a Pandas DataFrame
df = pd.read_csv(file_path)

# Convert all relevant columns to string
df = df.applymap(str)

# User input
user_description = input("Enter your course description: ")

# Convert user description to lowercase string
user_description = str(user_description).lower()

# Combine binary features and course descriptions for TF-IDF calculation
combined_data = df.apply(lambda x: ' '.join(map(str, x[4:16])) + ' ' + x['Description'].lower(), axis=1)

# Add user input to the combined_data
combined_data = combined_data.append(pd.Series(user_description, index=['UserInput']))

# Calculate TF-IDF vectors for descriptions and binary features
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(combined_data)

# Calculate cosine similarity between user input and course features
user_input_vector = tfidf_matrix[-1]  # User input is the last row
similarities = cosine_similarity(user_input_vector, tfidf_matrix[:-1]).flatten()

# Recommend top 10 electives based on similarity
recommendations = similarities.argsort()[:-3:-1]

# Display recommended electives
print("\nRecommended Electives:")
for index in recommendations:
    print(f"{df.at[index, 'Prefix']} {df.at[index, 'Number']} - {df.at[index, 'Title']}")