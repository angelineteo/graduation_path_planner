import pandas as pd
import customtkinter as ctk
import tkinter as tk
from academic_plan_backend import AcademicPlanGenerator

class AcademicPlanApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Academic Plan Generator")
        self.geometry("850x400")

        self.plan_generator = AcademicPlanGenerator("graduation_path_planner/Final_Spots_Updated_Modified_MockData.xlsx")

        # Dropdown for Concentrations
        self.concentration_label = ctk.CTkLabel(self, text="Select your concentration:")
        self.concentration_label.pack()

        self.concentration_combobox = ctk.CTkComboBox(self, values=self.plan_generator.get_concentrations())
        self.concentration_combobox.pack()

        # Slider for Class Size
        self.size_slider_label = ctk.CTkLabel(self, text="Preference for Class Size (Larger is on the Right):")
        self.size_slider_label.pack()

        self.size_slider = ctk.CTkSlider(self, from_=0, to=100, orientation='horizontal')
        self.size_slider.pack()

        # Slider for Difficulty
        self.diff_slider_label = ctk.CTkLabel(self, text="Preference for Difficulty (Larger is on the Right):")
        self.diff_slider_label.pack()

        self.diff_slider = ctk.CTkSlider(self, from_=0, to=100, orientation='horizontal')
        self.diff_slider.pack()

        # Slider for RMP Rating
        self.rtg_slider_label = ctk.CTkLabel(self, text="Preference for Rating (Better is on the Right):")
        self.rtg_slider_label.pack()

        self.rtg_slider = ctk.CTkSlider(self, from_=0, to=100, orientation='horizontal')
        self.rtg_slider.pack()

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate Plan", command=self.generate_plan)
        self.generate_button.pack()

        # Generate the output frame
        self.output_text = ctk.CTkTextbox(self)
        self.output_text.pack(fill='both', expand=True)

    def generate_plan(self):
        concentration = self.concentration_combobox.get()
        size_preference = self.size_slider.get()
        difficulty_preference = self.diff_slider.get()
        professor_preference = self.rtg_slider.get()
        plan = self.plan_generator.generate_academic_plan(concentration, size_preference, difficulty_preference, professor_preference)
        self.display_plan(plan)

    def display_plan(self, plan):
        # Clear existing content in the text box
        self.output_text.delete(1.0, tk.END)

        for semester, courses in enumerate(plan, start=1):
            # Add a header for each semester
            self.output_text.insert(tk.END, f"Semester {semester}:\n")

            # Assuming each course in courses is a dictionary with course details
            for course in courses:
                course_info = ", ".join(f"{key}: {value}" for key, value in course.items())
                self.output_text.insert(tk.END, course_info + "\n")

            # Add an extra line for spacing between semesters
            self.output_text.insert(tk.END, "\n")



if __name__ == "__main__":
    app = AcademicPlanApp()
    app.mainloop()
