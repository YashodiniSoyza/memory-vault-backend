import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from service import MemoryService, TherapyOutlineService, TherapyGenerationService
from play_therapy_window import open_play_therapy_window


class TherapyWindow:
    def __init__(self, parent, patient_id, patient_name):
        self.parent = parent
        self.patient_id = patient_id
        self.patient_name = patient_name

        self.memory_service = MemoryService()
        self.therapy_outline_service = TherapyOutlineService()
        self.therapy_generation_service = TherapyGenerationService()

        # Create Therapies Window
        self.create_window()

    def create_window(self):
        """
        Initializes the therapies window.
        """
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Therapies for {self.patient_name}")
        self.window.geometry("800x600")

        # Title
        ttk.Label(self.window, text=f"Therapies for {self.patient_name}", font=("Arial", 16)).pack(pady=20)

        # Scrollable Frame
        self.canvas = tk.Canvas(self.window)
        self.scroll_y = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # Load Memories and Therapy Outlines
        self.load_memories_and_therapies()

    def load_memories_and_therapies(self):
        """
        Fetches memories and associated therapy outlines for the selected patient.
        """
        try:
            memories = self.memory_service.get_memories_by_patient_id(self.patient_id)
            if not memories:
                messagebox.showinfo("Info", "No memories found for the selected patient.")
                return

            for memory in memories:
                therapy_outline = self.therapy_outline_service.get_therapy_outline_by_memory_id(memory.id)
                self.display_memory_card(memory, therapy_outline)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load memories and therapies: {e}")

    def display_memory_card(self, memory, therapy_outline):
        """
        Displays a single memory with its associated therapy outline in a card view.
        """
        # Create a frame for the memory card
        card_frame = ttk.Frame(self.scrollable_frame, relief="solid", padding=10)
        card_frame.pack(fill=tk.X, padx=10, pady=10, anchor="w")

        # Memory Title
        ttk.Label(card_frame, text=f"Memory: {memory.title}", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=5)

        # Therapy Outline Status
        if therapy_outline:
            ttk.Label(card_frame, text="Therapy Outline: Available", font=("Arial", 12), foreground="green").pack(anchor=tk.W)
        else:
            ttk.Label(card_frame, text="Therapy Outline: Not Available", font=("Arial", 12), foreground="red").pack(anchor=tk.W)

        # Buttons Frame
        buttons_frame = ttk.Frame(card_frame)
        buttons_frame.pack(anchor=tk.E, pady=5)

        # Generate Therapy Button
        generate_button = ttk.Button(
            buttons_frame,
            text="Generate Therapy",
            command=lambda: self.generate_therapy(therapy_outline),
            state="normal" if therapy_outline else "disabled"
        )
        generate_button.pack(side=tk.LEFT, padx=5)

        # Play Therapy Button
        play_button = ttk.Button(
            buttons_frame,
            text="Play Therapy",
            command=lambda: self.play_therapy(memory, therapy_outline),
            state="normal" if self._is_therapy_playable(therapy_outline) else "disabled"
        )
        play_button.pack(side=tk.LEFT, padx=5)

    def _is_therapy_playable(self, therapy_outline):
        """
        Checks if a therapy outline is playable (i.e., all steps have audio URLs).
        """
        if not therapy_outline or not therapy_outline.steps:
            return False
        return all(step.audio_url for step in therapy_outline.steps)

    def play_therapy(self, memory, therapy_outline):
        """
        Opens the Play Therapy window for the selected therapy outline.
        """
        if therapy_outline:
            open_play_therapy_window(self.window, memory, therapy_outline)
        else:
            messagebox.showinfo("Info", "No therapy outline available for this memory.")

    def generate_therapy(self, therapy_outline):
        """
        Generates therapy audio files for the given therapy outline.
        """
        def generate():
            try:
                # Show loading screen
                self.show_loading_screen()

                # Generate therapy
                self.therapy_generation_service.generate_voice_for_therapy_outline(therapy_outline.id)

                # Close loading screen and refresh
                self.hide_loading_screen()
                self.refresh_therapies()
                messagebox.showinfo("Info", f"Therapy generation completed for outline: {therapy_outline.id}")
            except Exception as e:
                self.hide_loading_screen()
                messagebox.showerror("Error", f"Failed to generate therapy: {e}")

        # Run the generation process in a separate thread
        Thread(target=generate).start()

    def show_loading_screen(self):
        """
        Displays a loading screen during therapy generation.
        """
        self.loading_screen = tk.Toplevel(self.window)
        self.loading_screen.title("Generating Therapy")
        self.loading_screen.geometry("300x100")
        ttk.Label(self.loading_screen, text="Generating therapy, please wait...", font=("Arial", 12)).pack(pady=20)
        self.loading_screen.grab_set()

    def hide_loading_screen(self):
        """
        Closes the loading screen.
        """
        if self.loading_screen:
            self.loading_screen.destroy()

    def refresh_therapies(self):
        """
        Refreshes the therapy display after generation.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.load_memories_and_therapies()


def open_therapy_window(parent, patient_id, patient_name):
    """
    Opens the therapies window.
    """
    TherapyWindow(parent, patient_id, patient_name)
