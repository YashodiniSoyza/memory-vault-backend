import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from pygame import mixer
from threading import Thread
from deepface import DeepFace
import cv2
import time


class PlayTherapyWindow:
    def __init__(self, parent, therapy_outline):
        self.parent = parent
        self.therapy_outline = therapy_outline
        self.current_step_index = 0
        self.emotion_data = {}

        # Initialize audio and camera
        mixer.init()
        self.video_capture = cv2.VideoCapture(0)
        self.running = True
        self.audio_playing = False

        # Create the therapy playback window
        self.create_window()

        # Start emotion detection
        Thread(target=self.update_emotion_detection).start()

    def create_window(self):
        """
        Initializes the play therapy window.
        """
        self.window = tk.Toplevel(self.parent)
        self.window.title("Play Therapy")
        self.window.geometry("1000x900")

        # Title
        self.title_label = ttk.Label(self.window, text="", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Description
        self.description_label = ttk.Label(self.window, text="", wraplength=700, font=("Arial", 12))
        self.description_label.pack(pady=10)

        # Image Display
        self.image_canvas = tk.Canvas(self.window, width=500, height=300, bg="gray")
        self.image_canvas.pack(pady=10)

        # Audio Player Controls
        self.play_button = ttk.Button(self.window, text="Play Audio", command=self.play_audio)
        self.play_button.pack(pady=5)

        # Navigation Buttons
        self.navigation_frame = ttk.Frame(self.window)
        self.navigation_frame.pack(pady=10)

        self.previous_button = ttk.Button(self.navigation_frame, text="Previous", command=self.previous_step)
        self.previous_button.grid(row=0, column=0, padx=5)

        self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self.next_step)
        self.next_button.grid(row=0, column=1, padx=5)

        # Camera Feed and Emotion Display (Positioned in lower-right corner)
        self.camera_frame = ttk.Frame(self.window)
        self.camera_frame.pack(side=tk.RIGHT, anchor=tk.SE, padx=20, pady=20)

        # Camera Feed
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(pady=5)

        # Emotion Label
        self.emotion_label = ttk.Label(self.camera_frame, text="Emotion: ", font=("Arial", 14))
        self.emotion_label.pack(pady=5)

        # Emotion Level Label
        self.emotion_level_label = ttk.Label(self.camera_frame, text="Emotion Level: ", font=("Arial", 12))
        self.emotion_level_label.pack(pady=5)

        # Load the first step
        self.load_step()

    def update_emotion_detection(self):
        """
        Updates the emotion detection in real time using webcam feed and records emotions during audio playback.
        """
        while self.running:
            ret, frame = self.video_capture.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                try:
                    # Analyze emotions
                    analysis = DeepFace.analyze(img_path=rgb_frame, actions=["emotion"], enforce_detection=False)
                    dominant_emotion = analysis[0]["dominant_emotion"]
                    emotion_confidence = analysis[0]["emotion"][dominant_emotion]

                    # Update emotion labels
                    self.emotion_label.config(text=f"Emotion: {dominant_emotion}")
                    self.emotion_level_label.config(text=f"Emotion Level: {emotion_confidence:.2f}")

                    # Update camera feed
                    img = Image.fromarray(rgb_frame)
                    img = img.resize((300, 200))
                    photo = ImageTk.PhotoImage(img)
                    self.camera_label.image = photo
                    self.camera_label.config(image=photo)

                    if self.audio_playing:
                        current_time = mixer.music.get_pos() // 1000
                        self.record_emotion(current_time, dominant_emotion, emotion_confidence)

                except Exception as e:
                    self.emotion_label.config(text="Emotion: Unable to detect")
                    self.emotion_level_label.config(text="Emotion Level: N/A")

    def record_emotion(self, current_time, emotion, confidence):
        """
        Records the emotion and its confidence level for the current step.
        """
        step = self.therapy_outline.steps[self.current_step_index]
        if step.audio_url not in self.emotion_data:
            self.emotion_data[step.audio_url] = []

        # Append the recorded emotion for the current timestamp
        self.emotion_data[step.audio_url].append({
            "time": current_time,
            "emotion": emotion,
            "confidence": confidence
        })

    def load_step(self):
        """
        Loads the current step into the UI.
        """
        step = self.therapy_outline.steps[self.current_step_index]

        # Set the title and description
        self.title_label.config(text=f"Step {step.step}: {step.description}")
        self.description_label.config(text="\n".join(step.guide))

        # Load the first image
        if step.media_urls:
            self.load_image(step.media_urls[0])
        else:
            self.image_canvas.delete("all")
            self.image_canvas.create_text(250, 150, text="No Image Available", font=("Arial", 14))

        # Update buttons
        self.update_buttons()

    def load_image(self, image_filename):
        """
        Loads and displays an image in the canvas.
        """
        try:
            image_path = os.path.join("images", image_filename)
            img = Image.open(image_path)
            img.thumbnail((500, 300))
            photo = ImageTk.PhotoImage(img)
            self.image_canvas.image = photo
            self.image_canvas.create_image(250, 150, image=photo)
        except FileNotFoundError:
            self.image_canvas.delete("all")
            self.image_canvas.create_text(250, 150, text="Error Loading Image", font=("Arial", 14))

    def play_audio(self):
        """
        Plays the audio associated with the current step.
        """
        step = self.therapy_outline.steps[self.current_step_index]
        if step.audio_url:
            audio_path = os.path.join("audio", step.audio_url)
            try:
                mixer.music.load(audio_path)
                mixer.music.play()
                self.audio_playing = True
                Thread(target=self.monitor_audio).start()  # Monitor when audio stops playing
            except Exception as e:
                messagebox.showerror("Error", f"Could not play audio: {e}")
        else:
            messagebox.showinfo("Info", "No audio available for this step.")

    def monitor_audio(self):
        """
        Monitors the audio playback and stops recording when the audio ends.
        """
        while mixer.music.get_busy():
            time.sleep(1)
        self.audio_playing = False

    def stop_audio(self):
        """
        Stops the currently playing audio.
        """
        if mixer.music.get_busy():
            mixer.music.stop()

    def previous_step(self):
        """
        Navigates to the previous step.
        """
        self.stop_audio()
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.load_step()

    def next_step(self):
        """
        Navigates to the next step or prompts for feedback if on the last step.
        """
        self.stop_audio()
        if self.current_step_index < len(self.therapy_outline.steps) - 1:
            self.current_step_index += 1
            self.load_step()
        else:
            self.prompt_feedback()

    def update_buttons(self):
        """
        Updates the state of navigation buttons based on the current step.
        """
        self.previous_button.config(state="normal" if self.current_step_index > 0 else "disabled")
        if self.current_step_index == len(self.therapy_outline.steps) - 1:
            self.next_button.config(text="Finish")
        else:
            self.next_button.config(text="Next")

    def prompt_feedback(self):
        """
        Prompts the user for feedback on the therapy session.
        """
        self.stop_audio()
        self.running = False
        self.video_capture.release()
        self.window.destroy()

        feedback_window = tk.Toplevel(self.parent)
        feedback_window.title("Feedback")
        feedback_window.geometry("400x300")

        ttk.Label(feedback_window, text="How did this session make you feel?", font=("Arial", 14)).pack(pady=20)

        feedback_var = tk.StringVar()
        for option in ["Very Happy", "Happy", "Neutral", "Sad"]:
            ttk.Radiobutton(feedback_window, text=option, value=option, variable=feedback_var).pack(anchor=tk.W, padx=20)

        ttk.Button(feedback_window, text="Submit", command=lambda: self.submit_feedback(feedback_var.get(), feedback_window)).pack(pady=20)

    def submit_feedback(self, feedback, feedback_window):
        """
        Handles the feedback submission.
        """
        feedback_window.destroy()
        messagebox.showinfo("Thank you", f"Your feedback '{feedback}' has been recorded!")
        print("Emotion Data:", self.emotion_data)
        mixer.music.stop()


def open_play_therapy_window(parent, memory, therapy_outline):
    """
    Opens the Play Therapy window for the selected therapy outline.
    """
    PlayTherapyWindow(parent, therapy_outline)
