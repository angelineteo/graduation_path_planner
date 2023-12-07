import pandas as pd
import numpy as np
import random
from collections import defaultdict

class AcademicPlanGenerator:
    def __init__(self):
        self.df_sections = pd.read_excel('graduation_path_planner/Final_Spots_Updated_Modified_MockData.xlsx')
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
        size_weight = size_preference / 100
        difficulty_weight = difficulty_preference / 5
        professor_weight = professor_preference / 5

        best_section = min(sections, key=lambda x: (-x[3] * size_weight + x[2] * difficulty_weight + x[1] * professor_weight))
        return best_section

    def get_concentrations(self):
        unique_sec = self.df_sections['Concentration'].unique()
        return unique_sec[2:]

    def calculate_difficulty_score(self, semester_plan):
        # Calculate the difficulty score for a semester
        return sum(self.class_credits[course['Course']] * course['RMP Difficulty'] for course in semester_plan)

    def generate_academic_plan(self, concentration, size_preference, difficulty_preference, professor_preference):
        self.parse_data(concentration)
        TOTAL_SEMESTERS = 8
        MAX_CREDITS_PER_SEMESTER = 18
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

        def find_best_semester_for_course(course):
            best_semester = None
            lowest_difficulty_increase = float('inf')
            for semester in range(TOTAL_SEMESTERS):
                if prereqs_met(course, semester) and self.class_credits[course] + sum(self.class_credits[course_detail['Course']] for course_detail in academic_plan[semester]) <= MAX_CREDITS_PER_SEMESTER:
                    current_difficulty = self.calculate_difficulty_score(academic_plan[semester])
                    temp_plan = academic_plan[semester].copy()
                    temp_plan.append({'Course': course, 'RMP Difficulty': self.class_sections[course][0][1], 'Credit Hours': self.class_credits[course]})
                    new_difficulty = self.calculate_difficulty_score(temp_plan)
                    difficulty_increase = new_difficulty - current_difficulty
                    if difficulty_increase < lowest_difficulty_increase:
                        best_semester = semester
                        lowest_difficulty_increase = difficulty_increase
            return best_semester

        for course in self.class_sections:
            if course in completed_courses:
                continue

            best_semester = find_best_semester_for_course(course)
            if best_semester is not None:
                chosen_section = self.choose_best_section(self.class_sections[course], size_preference, difficulty_preference, professor_preference)
                class_id, rmp_difficulty, spots_available, rmp_rating = chosen_section
                course_concentration = self.df_sections[self.df_sections['Class ID'] == class_id]['Concentration'].iloc[0]
                professor_name = self.df_sections[self.df_sections['Class ID'] == class_id]['Instructor'].iloc[0]
                class_name = self.df_sections[self.df_sections['Class ID'] == class_id]['Class Name'].iloc[0]

                academic_plan[best_semester].append({
                    'Course': course,
                    'Class ID': class_id,
                    'Class Name': class_name,
                    'Professor': professor_name,
                    'RMP Difficulty': rmp_difficulty,
                    'Credit Hours': self.class_credits[course],
                    'Class Size': spots_available,
                    'RMP Rating': round(rmp_rating, 2),
                    'Concentration': course_concentration,
                })
                completed_courses.add(course)

        return academic_plan

# Example usage:
# plan_generator = AcademicPlanGenerator()
# concentration = 'Your Concentration'
# size_preference = 50  # Example value
# difficulty_preference = 10  # Example value
# professor_preference = 10  # Example value
# academic_plan = plan_generator.generate_academic_plan(concentration, size_preference, difficulty_preference, professor_preference)
