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
            self.class_sections[row['Class Code']].append((row['Class ID'], row['RMP Difficulty'], row['Spots Available']))
        
        self.prereqs = {row['Class Code']: row['Prereq code'] for _, row in prereqs.iterrows()}

    @staticmethod
    def choose_best_section(sections, size_preference, difficulty_preference, professor_preference):
        # Normalize slider values
        size_weight = size_preference / 100
        difficulty_weight = difficulty_preference/ 20
        professor_weight = professor_preference / 20

        # Determine the best section based on weighted criteria
        best_section = min(sections, key=lambda x: (-x[2] * size_weight + x[1] * difficulty_weight - x[0] * professor_weight))
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
                if any(prereq == c for c, _ in academic_plan[past_semester]):
                    return True
            return False

        for semester in range(TOTAL_SEMESTERS):
            for course in self.class_sections:
                if course in completed_courses:
                    continue
                if course in self.class_credits and self.class_credits[course] + sum(self.class_credits[c] for c, _ in academic_plan[semester]) <= MAX_CREDITS_PER_SEMESTER and prereqs_met(course, semester):
                    chosen_section = self.choose_best_section(self.class_sections[course], size_preference, difficulty_preference, professor_preference)
                academic_plan[semester].append((course, chosen_section))
                completed_courses.add(course)

        return academic_plan
