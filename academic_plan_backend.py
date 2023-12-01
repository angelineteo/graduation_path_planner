import sys
import pandas as pd
import numpy as np
import random
from collections import defaultdict

class AcademicPlanGenerator:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df_sections = pd.read_excel(data_file)
        self.class_credits = {}
        self.class_sections = {}
        self.prereqs = {}

    def parse_data(self, concentration):
        classes = self.df_sections[(self.df_sections['Concentration'] == concentration) | (self.df_sections['Concentration'] == 'Required')]
        prereqs = classes[['Prereq code', 'Class Code']].dropna().drop_duplicates()

        self.class_credits = {row['Class Code']: row['Credit Hours'] for _, row in classes.iterrows()}
        self.class_sections = {row['Class Code']: [] for _, row in classes.iterrows()}
        for _, row in classes.iterrows():
            self.class_sections[row['Class Code']].append((row['Class ID'], row['RMP Difficulty'], row['Spots Available'], row['Rate my Professor Ratings']))
        
        self.prereqs = {row['Class Code']: row['Prereq code'] for _, row in prereqs.iterrows()}

    @staticmethod
    def choose_best_section(sections, size_preference, difficulty_preference, professor_preference):
        # Normalize slider values
        size_weight = size_preference / 100
        difficulty_weight = difficulty_preference/ 20
        professor_weight = professor_preference / 20

        # Determine the best section based on weighted criteria
        best_section = min(sections, key=lambda x: (-x[3] * size_weight + x[2] * difficulty_weight + x[1] * professor_weight))

        return best_section

    def get_concentrations(self):
        unique_sec = self.df_sections['Concentration'].unique()
        return unique_sec[2:]

    def generate_academic_plan(self, concentration, size_preference, difficulty_preference, professor_preference):
        self.parse_data(concentration)
        TOTAL_SEMESTERS = 8
        MAX_CREDITS_PER_SEMESTER = 17
        academic_plan = [[] for _ in range(TOTAL_SEMESTERS)]
        completed_courses = set()
        self.parse_data(concentration)
        
        TOTAL_SEMESTERS = 8
        MAX_CREDITS_PER_SEMESTER = 17
        academic_plan = [[] for _ in range(TOTAL_SEMESTERS)]
        completed_courses = set()

        def prereqs_met(course, semester):
            prereq = self.prereqs.get(course)
            if not prereq:
                return True
            for past_semester in range(semester):
               if any(prereq == course_detail['Course'] for course_detail in academic_plan[past_semester]):
                    return True
            return False

        for semester in range(TOTAL_SEMESTERS):
            for course in self.class_sections:
                if course in completed_courses:
                    continue
                if course in self.class_credits and self.class_credits[course] + sum(self.class_credits[course_detail['Course']] for course_detail in academic_plan[semester]) <= MAX_CREDITS_PER_SEMESTER and prereqs_met(course, semester):
                    chosen_section = self.choose_best_section(self.class_sections[course], size_preference, difficulty_preference, professor_preference)
                    
                    # Extract details from chosen_section
                    class_id, rmp_difficulty, spots_available, rmp_rating = chosen_section
                    course_concentration = self.df_sections[self.df_sections['Class ID'] == class_id]['Concentration'].iloc[0]

                    # Extract professor's name
                    professor_name = self.df_sections[self.df_sections['Class ID'] == class_id]['Instructor'].iloc[0]

                    # Extract class name
                    class_name = self.df_sections[self.df_sections['Class ID'] == class_id]['Class Name'].iloc[0]

                    # Append detailed information
                    academic_plan[semester].append({
                        'Course': course,
                        'Class ID': class_id,
                        'Class Name': class_name,
                        'Professor': professor_name,
                        'RMP Difficulty': rmp_difficulty,
                        'Class Size': spots_available,
                        'RMP Rating': round(rmp_rating, 2),
                        'Concentration': course_concentration,
                    })
                    completed_courses.add(course)

        return academic_plan
