import pandas as pd
import customtkinter as ctk
import tkinter
from academic_plan_backend import AcademicPlanGenerator

class AcademicPlanApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Academic Plan Generator")
        self.geometry("600x400")

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

        # Output Text Area
        self.output_text = ctk.CTkTextbox(self, height=10, width=50)
        self.output_text.pack()

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate Plan", command=self.generate_plan)
        self.generate_button.pack()

    def generate_plan(self):
        concentration = self.concentration_combobox.get()
        size_preference = self.size_slider.get()
        difficulty_preference = self.diff_slider.get()
        professor_preference = self.rtg_slider.get()
        plan = self.plan_generator.generate_academic_plan(concentration, size_preference, difficulty_preference, professor_preference)
        self.display_plan(plan)

    def display_plan(self, plan):
        self.output_text.delete(1.0, ctk.END)
        for semester, courses in enumerate(plan, start=1):
            self.output_text.insert(ctk.END, f"Semester {semester}: {', '.join(courses)}\n")

if __name__ == "__main__":
    app = AcademicPlanApp()
    app.mainloop()
