import customtkinter as ctk
from tkinter import scrolledtext
from elective_picker import ElectivePicker  # Import your ElectivePicker class

class ElectivePickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Elective Course Picker")
        self.geometry("600x500")

        self.picker = ElectivePicker()  # Initialize your ElectivePicker

        # Interest Input
        self.interest_label = ctk.CTkLabel(self, text="Enter your interests:")
        self.interest_label.pack(pady=10)
        self.interest_text = ctk.CTkTextbox(self, width=400, height=100, corner_radius=10)
        self.interest_text.pack(pady=10)

        # Buttons
        self.get_recommendations_button = ctk.CTkButton(self, text="Get Recommendations", command=self.get_recommendations)
        self.get_recommendations_button.pack(pady=10)

        # Display Recommendations
        self.recommendations_label = ctk.CTkLabel(self, text="Recommended Courses:")
        self.recommendations_label.pack(pady=10)
        self.recommendations_display = scrolledtext.ScrolledText(self, height=60, width=120)
        self.recommendations_display.pack(pady=10)

    def get_recommendations(self):
        interest = self.interest_text.get("1.0", "end-1c")  # Get interest input
        self.picker.set_interest(interest)  # Set interest in picker
        recommendations = self.picker.get_recommendations()  # Get recommendations
        self.display_recommendations(recommendations)

    def display_recommendations(self, recommendations):
        self.recommendations_display.delete('1.0', ctk.END)  # Clear previous recommendations
        for index, row in recommendations.iterrows():
            self.recommendations_display.insert(ctk.END, f"{row['Title']} - Similarity: {row['Similarity']}, Rating: {row['Rating']}\n")

if __name__ == "__main__":
    app = ElectivePickerApp()
    app.mainloop()
