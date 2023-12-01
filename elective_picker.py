import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

class ElectivePicker:

    def __init__(self, filepath):
        self.course_list = pd.read_csv("graduation_path_planner/formatted_refined_table.csv")
        self.interest_paragraph = None
        self.tfidf = None


    def set_interest(self, paragraph):
        self.interest_paragraph = paragraph

    def calculate_similarity(self):
        if self.interest_paragraph is None or self.course_list is None:
            raise ValueError("Interest paragraph or course list is not set")

        titles = pd.Series(self.course_list["Title"])
        data = pd.concat([pd.Series(self.interest_paragraph), titles])
        self.tfidf = TfidfVectorizer().fit_transform(data)
        cosine_sim = linear_kernel(self.tfidf[0:1], self.tfidf).flatten()
        return pd.DataFrame({'Title': titles, 'Similarity': cosine_sim[1:]})

    def get_recommendations(self):
        df_similarity = self.calculate_similarity()
        df_sorted = df_similarity.sort_values(by='Similarity', ascending=False)
        return df_sorted.head(20)

    def set_liked_courses(self, liked_courses):
        self.liked_courses = liked_courses

    def perform_clustering(self, n_clusters=86):
        # Normalize the TF-IDF vectors
        normalized_vectors = normalize(self.tfidf)
        
        # KMeans Clustering
        self.kmeans = KMeans(n_clusters=n_clusters)
        self.kmeans.fit(normalized_vectors)

        # Storing the cluster each title belongs to
        correct_labels = self.kmeans.labels_[self.course_list.index]
        self.course_list['Cluster'] = correct_labels

    def get_cluster_based_recommendations(self):
        if self.liked_courses is None:
            raise ValueError("Liked courses not set")

        # Find the clusters of the liked courses
        liked_clusters = self.course_list[self.course_list['Title'].isin(self.liked_courses)]['Cluster']
        
        # Recommend courses from the same clusters
        recommendations = self.course_list[self.course_list['Cluster'].isin(liked_clusters)]
        return recommendations.drop_duplicates().head(20)

# Usage
picker = ElectivePicker("graduation_path_planner/formatted_refined_table.csv")
picker.set_interest("I am interested in  data analysis, movies, art, buildings, visualization, design")
initial_recommendations = picker.get_recommendations()

# Assuming the user likes some of these courses
picker.set_liked_courses(['Mathematics of Art 1', 'Data Storytelling'])  # Replace with actual course titles chosen by the user
picker.perform_clustering()
further_recommendations = picker.get_cluster_based_recommendations()

print(initial_recommendations)