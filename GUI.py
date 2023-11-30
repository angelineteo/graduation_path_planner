import pandas as pd
import customtkinter as ctk
from academic_plan_backend import AcademicPlanGenerator

class AcademicPlanApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Academic Plan Generator")
        self.geometry("600x400")

        self.plan_generator = AcademicPlanGenerator("FinalProj/Final_Spots_Updated_Modified_MockData.xlsx")

        # Dropdown for Concentrations
        self.concentration_label = ctk.CTkLabel(self, text="Select your concentration:")
        self.concentration_label.pack()

        self.concentration_combobox = ctk.CTkComboBox(self, values=self.plan_generator.get_concentrations())
        self.concentration_combobox.pack()

        # Slider for Difficulty vs Class Size
        self.slider_label = ctk.CTkLabel(self, text="Preference (Left: Easier, Right: Smaller Class Size):")
        self.slider_label.pack()

        self.slider = ctk.CTkSlider(self, from_=0, to=100, orient='horizontal')
        self.slider.pack()

        # Output Text Area
        self.output_text = ctk.CTkTextbox(self, height=10, width=50)
        self.output_text.pack()

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate Plan", command=self.generate_plan)
        self.generate_button.pack()

    def generate_plan(self):
        concentration = self.concentration_combobox.get()
        preference = self.slider.get()
        plan = self.plan_generator.generate_plan(concentration, preference)
        self.display_plan(plan)

    def display_plan(self, plan):
        self.output_text.delete(1.0, ctk.END)
        for semester, courses in enumerate(plan, start=1):
            self.output_text.insert(ctk.END, f"Semester {semester}: {', '.join(courses)}\n")

if __name__ == "__main__":
    app = AcademicPlanApp()
    app.mainloop()
