import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from service import PatientService, MemoryService
from therapy_window import open_therapy_window


class TherapyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Therapy Generation System")
        self.root.geometry("800x600")

        self.patient_service = PatientService()
        self.memory_service = MemoryService()

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        ttk.Label(self.root, text="Therapy Generation System", font=("Arial", 20)).pack(pady=20)

        # Patient Dropdown
        ttk.Label(self.root, text="Select Patient:", font=("Arial", 14)).pack(pady=5)
        self.patient_combobox = ttk.Combobox(self.root, state="readonly", font=("Arial", 12), width=50)
        self.patient_combobox.pack(pady=10)
        self.patient_combobox.bind("<<ComboboxSelected>>", self.on_patient_selected)

        # View Memories Button
        self.view_memories_button = ttk.Button(
            self.root,
            text="View Memories",
            command=self.view_memories,
            state="disabled"
        )
        self.view_memories_button.pack(pady=10)

        # View Therapies Button
        self.view_therapies_button = ttk.Button(
            self.root,
            text="View Therapies",
            command=self.view_therapies,
            state="disabled"
        )
        self.view_therapies_button.pack(pady=10)

        # Load Patients
        self.load_patients()

    def load_patients(self):
        """
        Fetches all patients from the database and populates the dropdown.
        """
        try:
            patients = self.patient_service.get_all_patients()
            if not patients:
                messagebox.showinfo("Info", "No patients found.")
                return

            # Map patient names to their IDs
            self.patients = {patient.name: patient.id for patient in patients}
            self.patient_combobox["values"] = list(self.patients.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")

    def on_patient_selected(self, event):
        """
        Enables the buttons when a patient is selected.
        """
        self.selected_patient = self.patient_combobox.get()
        if self.selected_patient:
            self.view_memories_button["state"] = "normal"
            self.view_therapies_button["state"] = "normal"

    def view_memories(self):
        """
        Fetches and displays the memories of the selected patient in a new scrollable window.
        """
        try:
            patient_id = self.patients[self.selected_patient]
            memories = self.memory_service.get_memories_by_patient_id(patient_id)

            if not memories:
                messagebox.showinfo("Info", "No memories found for the selected patient.")
                return

            # Open a new window to display memories
            memories_window = tk.Toplevel(self.root)
            memories_window.title(f"Memories of {self.selected_patient}")
            memories_window.geometry("800x600")

            # Create a scrollable frame
            canvas = tk.Canvas(memories_window)
            scroll_y = ttk.Scrollbar(memories_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)

            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            # Display each memory in the scrollable frame
            for memory in memories:
                self.display_memory(scrollable_frame, memory)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load memories: {e}")

    def display_memory(self, parent, memory):
        """
        Displays a single memory with its images, descriptions, and metadata in a card-like style.
        """
        # Create a frame for the memory (card style)
        memory_frame = ttk.Frame(parent, relief="solid", padding=10)
        memory_frame.pack(fill=tk.X, padx=10, pady=10, anchor="w")

        # Title
        ttk.Label(memory_frame, text=f"Memory: {memory.title}", font=("Arial", 14, "bold")).pack(anchor=tk.W)

        # Description
        ttk.Label(memory_frame, text=memory.description, font=("Arial", 12), wraplength=700, justify="left").pack(anchor=tk.W, pady=5)

        # Display metadata as comma-separated values
        self.display_metadata(memory_frame, "Categories", memory.categories)
        self.display_metadata(memory_frame, "Emotions", memory.emotions)
        self.display_metadata(memory_frame, "Tags", memory.tags)

        # Display images with descriptions
        for media in memory.media:
            if media.type == "Image":
                self.display_image_with_description(memory_frame, media)

    def display_image_with_description(self, parent, media):
        """
        Displays an image with its description in a separate frame.
        """
        image_frame = ttk.Frame(parent, relief="solid", padding=5)
        image_frame.pack(fill=tk.X, padx=5, pady=5, anchor="w")

        try:
            # Load and display image
            image_path = os.path.join("images", media.url)
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # Resize image for display
            img_tk = ImageTk.PhotoImage(img)

            image_label = ttk.Label(image_frame, image=img_tk)
            image_label.image = img_tk  # Keep a reference to avoid garbage collection
            image_label.pack(side=tk.LEFT, padx=5)

        except FileNotFoundError:
            messagebox.showwarning("Warning", f"Image not found: {media.url}")
            return

        # Display description beside the image
        ttk.Label(image_frame, text=media.description, font=("Arial", 12), wraplength=500, justify="left").pack(side=tk.LEFT, padx=10)

    def display_metadata(self, parent, label, items):
        """
        Displays metadata as comma-separated text under a specified label.
        """
        if items:
            ttk.Label(parent, text=f"{label}: {', '.join(items)}", font=("Arial", 12, "italic")).pack(anchor=tk.W, pady=2)

    def view_therapies(self):
        """
        Opens the therapies window for the selected patient.
        """
        patient_id = self.patients[self.selected_patient]
        open_therapy_window(self.root, patient_id, self.selected_patient)


if __name__ == "__main__":
    root = tk.Tk()
    app = TherapyApp(root)
    root.mainloop()
