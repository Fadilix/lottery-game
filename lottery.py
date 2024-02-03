import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from random import sample
import json
from datetime import datetime

class LotteryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("JEU DE LOTERIE")
        self.master.configure(bg='#222222')  # Dark mode by default

        self.dark_mode = tk.BooleanVar(value=True)

        # Custom Header Frame
        self.header_frame = ttk.Frame(self.master, style='Header.TFrame')
        self.header_frame.grid(row=0, column=0, columnspan=10, pady=(20, 30), sticky='ew')

        # Custom Header Label
        header_label = ttk.Label(self.header_frame, text="JEU DE LOTERIE", font=('Helvetica', 24, 'bold'), style='Header.TLabel')
        header_label.grid(row=0, column=0, pady=10, sticky='nsew')

        # Help Button
        help_button = ttk.Button(self.master, text="Aide", command=self.show_help, style='Help.TButton')
        help_button.grid(row=0, column=9, pady=(20, 30), padx=(0, 20), sticky='e')

        # New menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Game", command=self.save_game)
        file_menu.add_command(label="Load Game", command=self.load_game)

        # History menu
        history_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="History", menu=history_menu)
        history_menu.add_command(label="View History", command=self.view_history)

        self.buttons = []
        self.selected_buttons = set()
        self.score = 0
        self.history_log = []
        self.double_points = False  # Flag for double points surprise

        # Creation of buttons from 1 to 99
        for i in range(1, 100):
            button = tk.Button(self.master, text=str(i), command=lambda i=i: self.select_button(i),
                               width=3, height=2, font=('Helvetica', 10, 'bold'),
                               relief='flat', bg='#333333' if self.dark_mode.get() else '#DDDDDD',
                               fg='white' if self.dark_mode.get() else '#333333')
            button.grid(row=(i) // 10 + 1, column=(i) % 10, padx=5, pady=5, sticky='nsew')
            self.buttons.append(button)

        # Button to draw winning numbers
        draw_button = ttk.Button(self.master, text="Tirage", command=self.draw_numbers, style='Draw.TButton')
        draw_button.grid(row=12, column=5, pady=(10, 20), sticky='nsew')

        # Score
        self.score_label = ttk.Label(self.master, text="Score: 0", font=('Helvetica', 12), style='Score.TLabel')
        self.score_label.grid(row=13, column=5, sticky='nsew')

        # Button to switch light/dark mode
        mode_button = ttk.Checkbutton(self.master, text="Dark Mode", variable=self.dark_mode,
                                      command=self.toggle_mode, style='Mode.TCheckbutton')
        mode_button.grid(row=0, column=8, pady=(20, 30), padx=(0, 20), sticky='e')

        # Apply the initial theme
        self.setup_styles()
        self.toggle_mode()

        # Configure column and row weights for expansion
        for i in range(10):
            self.master.columnconfigure(i, weight=1)
        for i in range(14):
            self.master.rowconfigure(i, weight=1)

    def select_button(self, number):
        if len(self.selected_buttons) < 5:
            self.selected_buttons.add(number)
            self.buttons[number - 1].config(
                bg='#FFD700' if self.dark_mode.get() else '#FFA500',
                fg='#333333' if self.dark_mode.get() else 'white'
            )

    def draw_numbers(self):
        if len(self.selected_buttons) == 5:
            # Drawing 5 random numbers
            winning_numbers = sample(range(1, 100), 5)

            # Checking for winnings
            winnings = len(self.selected_buttons.intersection(winning_numbers)) * 10000

            # Apply double points surprise
            if self.double_points:
                winnings *= 2
                self.double_points = False  # Reset the flag after applying

            self.score += winnings

            # Displaying results
            result_message = f"Numéros gagnants : {winning_numbers}\nGains : {winnings} points"
            messagebox.showinfo("Résultats du tirage", result_message)

            # Update history log
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.history_log.append(f"{timestamp}: {result_message}")

            # Resetting buttons and updating the score
            self.reset_buttons()
            self.update_score()

            if len(self.selected_buttons) == 5 and winnings == 50000:
                messagebox.showinfo("Félicitations !", "Vous avez remporté le jackpot !")

    def reset_buttons(self):
        for button in self.buttons:
            button.config(
                bg='#333333' if self.dark_mode.get() else '#DDDDDD',
                fg='white' if self.dark_mode.get() else '#333333'
            )
        self.selected_buttons.clear()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def toggle_mode(self):
        theme = 'xpnative' if self.dark_mode.get() else 'default'
        ttk.Style().theme_use(theme)
        self.master.configure(bg='#222222' if self.dark_mode.get() else '#DDDDDD')

        # Update custom header
        self.header_frame.configure(style='HeaderDark.TFrame' if self.dark_mode.get() else 'Header.TFrame')

        # Update score label
        self.score_label.configure(style='ScoreDark.TLabel' if self.dark_mode.get() else 'Score.TLabel')

    def setup_styles(self):
        ttk.Style().configure('Header.TFrame', background='#4CAF50')
        ttk.Style().configure('HeaderDark.TFrame', background='#222222')

        ttk.Style().configure('Header.TLabel', font=('Helvetica', 24, 'bold'), foreground='#FFD700', background='#4CAF50')
        ttk.Style().configure('Score.TLabel', font=('Helvetica', 12), foreground='#FFD700', background='#DDDDDD')
        ttk.Style().configure('ScoreDark.TLabel', font=('Helvetica', 12), foreground='#FFD700', background='#333333')

        ttk.Style().configure('Draw.TButton', font=('Helvetica', 14, 'bold'), background='#4CAF50', foreground='white')
        ttk.Style().configure('Mode.TCheckbutton', font=('Helvetica', 10), background='#DDDDDD', foreground='#4CAF50')

        ttk.Style().configure('Help.TButton', font=('Helvetica', 10), background='#DDDDDD', foreground='#4CAF50')

    def show_help(self):
        help_text = "Bienvenue dans le JEU DE LOTERIE !\n\nCliquez sur les numéros pour les sélectionner.\n\
        Une fois que vous avez sélectionné 5 numéros, cliquez sur le bouton 'Tirage'.\n\
        Si vos numéros correspondent aux numéros gagnants, vous gagnez des points !\n\
        Atteignez 50 000 points pour remporter le jackpot !"
        messagebox.showinfo("Aide", help_text)

    def save_game(self):
        save_data = {
            'selected_buttons': list(self.selected_buttons),
            'score': self.score,
            'dark_mode': self.dark_mode.get()
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(save_data, file)
            messagebox.showinfo("Save Successful", "Game saved successfully.")

    def load_game(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                load_data = json.load(file)

            self.reset_buttons()
            self.selected_buttons = set(load_data['selected_buttons'])
            self.score = load_data['score']
            self.update_score()

            self.dark_mode.set(load_data['dark_mode'])
            self.toggle_mode()

            messagebox.showinfo("Load Successful", "Game loaded successfully.")

    def view_history(self):
        if not self.history_log:
            messagebox.showinfo("No History", "No history available.")
            return

        history_text = "\n".join(self.history_log)
        messagebox.showinfo("Game History", history_text)

    def show_surprise(self):
        # Add a surprise feature here
        self.double_points = True
        messagebox.showinfo("Surprise!", "Double Points activated for the next draw!")

if __name__ == "__main__":
    root = tk.Tk()
    game = LotteryGame(root)
    root.mainloop()