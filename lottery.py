import tkinter as tk
from tkinter import ttk, messagebox
from random import sample

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

        self.buttons = []
        self.selected_buttons = set()
        self.score = 0

        # Creation of buttons from 1 to 99
        for i in range(1, 100):
            button = tk.Button(self.master, text=str(i), command=lambda i=i: self.select_button(i), width=3, height=2, font=('Helvetica', 10, 'bold'), relief='flat', bg='#333333' if self.dark_mode.get() else '#DDDDDD', fg='white' if self.dark_mode.get() else '#333333')
            button.grid(row=(i) // 10 + 1, column=(i) % 10, padx=5, pady=5, sticky='nsew')
            self.buttons.append(button)

        # Button to draw winning numbers
        draw_button = ttk.Button(self.master, text="Tirage", command=self.draw_numbers, style='Draw.TButton')
        draw_button.grid(row=12, column=5, pady=(10, 20), sticky='nsew')

        # Score
        self.score_label = ttk.Label(self.master, text="Score: 0", font=('Helvetica', 12), style='Score.TLabel')
        self.score_label.grid(row=13, column=5, sticky='nsew')

        # Button to switch light/dark mode
        mode_button = ttk.Checkbutton(self.master, text="Dark Mode", variable=self.dark_mode, command=self.toggle_mode, style='Mode.TCheckbutton')
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
            self.buttons[number - 1].config(bg='#FFD700' if self.dark_mode.get() else '#FFA500', fg='#333333' if self.dark_mode.get() else 'white')

    def draw_numbers(self):
        if len(self.selected_buttons) == 5:
            # Drawing 5 random numbers
            winning_numbers = sample(range(1, 100), 5)

            # Checking for winnings
            winnings = len(self.selected_buttons.intersection(winning_numbers)) * 10000
            self.score += winnings

            # Displaying results
            result_message = f"Numéros gagnants : {winning_numbers}\nGains : {winnings} points"
            messagebox.showinfo("Résultats du tirage", result_message)

            # Resetting buttons and updating the score
            self.reset_buttons()
            self.update_score()

            if len(self.selected_buttons) == 5 and winnings == 50000:
                messagebox.showinfo("Félicitations !", "Vous avez remporté le jackpot !")

    def reset_buttons(self):
        for button in self.buttons:
            button.config(bg='#333333' if self.dark_mode.get() else '#DDDDDD', fg='white' if self.dark_mode.get() else '#333333')
        self.selected_buttons.clear()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def toggle_mode(self):
        theme = 'clam' if self.dark_mode.get() else 'default'
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

if __name__ == "__main__":
    root = tk.Tk()
    game = LotteryGame(root)
    root.mainloop()
