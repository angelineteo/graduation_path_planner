import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

class ElectivePicker:

    def __init__(self):
        self.course_list = pd.read_csv("graduation_path_planner/NUPath_data.csv")
        self.interest_paragraph = None
        self.tfidf = None
        self.liked_courses = None
        self.kmeans = None

    def set_interest(self, paragraph):
        self.interest_paragraph = paragraph

    def calculate_similarity(self):
        if self.interest_paragraph is None or self.course_list is None:
            raise ValueError("Interest paragraph or course list is not set")

        titles = self.course_list["Title"]
        descriptions = self.course_list["Description"]
        combined_texts = titles + " " + descriptions  # Combine titles and descriptions

        data = pd.concat([pd.Series(self.interest_paragraph), combined_texts])
     
        self.tfidf = TfidfVectorizer().fit_transform(data)
        cosine_sim = linear_kernel(self.tfidf[0:1], self.tfidf).flatten()
        return pd.DataFrame({'Title': titles, 'Similarity': cosine_sim[1:], 'Rating': self.course_list['Rating']})

    def get_recommendations(self):
        df_similarity = self.calculate_similarity()
        df_sorted = df_similarity.sort_values(by=['Similarity', 'Rating'], ascending=[False, False])
        return df_sorted.head(30)

    def set_liked_courses(self, liked_courses):
        self.liked_courses = liked_courses

    def perform_clustering(self, n_clusters=120):
        normalized_vectors = normalize(self.tfidf)
        self.kmeans = KMeans(n_clusters=n_clusters)
        self.kmeans.fit(normalized_vectors)
        correct_labels = self.kmeans.labels_[self.course_list.index]
        self.course_list['Cluster'] = correct_labels

    def get_cluster_based_recommendations(self):
        if self.liked_courses is None:
            raise ValueError("Liked courses not set")

        liked_clusters = self.course_list[self.course_list['Title'].isin(self.liked_courses)]['Cluster']
        recommendations = self.course_list[self.course_list['Cluster'].isin(liked_clusters)]
        recommendations = recommendations.drop_duplicates().sort_values(by='Rating', ascending=False)
        return recommendations.head(50)