import tkinter as tk
from Genshin_Artifact import *
from tkinter import ttk, messagebox
from Artifacts_UpgradeLogic import Framing_Artifacts, farm_for_characters
import threading

class ArtifactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Genshin Artifact Simulator")
        self.root.geometry("620x550")
        self.root.configure(bg="#f7f9fb")

        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", font=("Helvetica", 10), borderwidth=0)
        style.map("TButton", background=[("active", "#e1ecf4")])

        # Title
        title = ttk.Label(root, text="Genshin Artifact Farming Simulator", font=("Helvetica", 20, "bold"), background="#f7f9fb")
        title.pack(pady=20)

        # Input Frame
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Character Name:").grid(row=0, column=0, padx=10, pady=5)
        self.char_entry = ttk.Entry(frame, width=20)
        self.char_entry.insert(0, "Diluc")
        self.char_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Artifact Set:").grid(row=1, column=0, padx=10, pady=5)
        self.suit_entry = ttk.Entry(frame, width=20)
        self.suit_entry.insert(0, "Mo nv")
        self.suit_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.run_button = ttk.Button(button_frame, text="Farm 1 Character to Graduate", command=self.run_simulation)
        self.run_button.grid(row=0, column=0, padx=10, pady=5)

        self.multi_button = ttk.Button(button_frame, text="Graduate 100 Characters!", command=self.run_multi_simulation_thread)
        self.multi_button.grid(row=0, column=1, padx=10, pady=5)

        # Output Box
        self.output = tk.Text(root, height=20, width=75, font=("Consolas", 10), bg="#ffffff", bd=1, relief="solid")
        self.output.pack(pady=15)
        self.output.config(state=tk.DISABLED)

    def run_simulation(self):
        character = self.char_entry.get()
        suit = self.suit_entry.get()

        try:
            log = Framing_Artifacts(target=character, suit=suit, display=False)
            graduate_dict, best_artifacts, count = log

            output_text = f"Character: {character}\nSuit: {suit}\n"
            output_text += f"Graduated Positions: {graduate_dict}\n"
            output_text += "Best Artifacts:\n"
            
            artifact:Artifact
            for artifact in filter(None, best_artifacts):
                output_text += f"  {artifact.position}: {artifact.main_attribute}, {artifact.sub_attributes}\n"
            output_text += f"Total farming attempts: {count}\n"

            self.display_output(output_text)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_multi_simulation_thread(self):
        thread = threading.Thread(target=self.run_multi_simulation)
        thread.start()

    def run_multi_simulation(self):
        try:
            self.display_output("Running 100 simulations. Please wait...\n")
            total_count = 0
            n = 100
            for i in range(n):
                count = Framing_Artifacts(display=False)[2]
                total_count += count
            avg = total_count // n
            self.display_output(f"Average farm times for every character: {avg}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ArtifactApp(root)
    root.mainloop()
