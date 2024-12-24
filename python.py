import tkinter as tk
import random
from tkinter import messagebox

class MinesGame:
    def __init__(self, root, switch_game_callback):
        self.root = root
        self.switch_game_callback = switch_game_callback
        self.frame = tk.Frame(root, bg="#2C3E50")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Game variables
        self.starting_money = 1000
        self.money = self.starting_money
        self.bet = 0
        self.grid_size = 5
        self.multiplier = 1.0
        self.mines = []
        self.revealed = []
        self.level = 1

        # Top frame for money and level
        self.top_frame = tk.Frame(self.frame, bg="#2C3E50")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.money_label = tk.Label(self.top_frame, text=f"Money: ${self.money}", font=("Arial", 16), bg="#2C3E50", fg="white")
        self.money_label.pack(side=tk.LEFT, padx=10)

        self.level_label = tk.Label(self.top_frame, text=f"Level: {self.level}", font=("Arial", 16), bg="#2C3E50", fg="white")
        self.level_label.pack(side=tk.LEFT, padx=10)

        # Side frame for level selection
        self.side_frame = tk.Frame(self.frame, bg="#34495E", width=200)
        self.side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.level_frame = tk.LabelFrame(self.side_frame, text="Select Level", font=("Arial", 14), bg="#34495E", fg="white")
        self.level_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.level_buttons = []
        self.create_level_section()

        self.switch_game_button = tk.Button(
            self.side_frame, text="Switch Game", font=("Arial", 12), bg="#1ABC9C", fg="white", command=self.switch_game_callback
        )
        self.switch_game_button.pack(pady=20)

        # Main frame for the game grid and controls
        self.main_frame = tk.Frame(self.frame, bg="#2C3E50")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.grid_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.grid_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.controls_frame = tk.Frame(self.main_frame, bg="#2C3E50")
        self.controls_frame.pack(fill=tk.X, pady=10)

        self.bet_entry = tk.Entry(self.controls_frame, font=("Arial", 14), justify="center")
        self.bet_entry.pack(side=tk.LEFT, padx=10)
        self.bet_entry.insert(0, "Enter bet amount")

        self.bet_button = tk.Button(self.controls_frame, text="Place Bet", font=("Arial", 14), bg="#3498DB", fg="white", command=self.place_bet)
        self.bet_button.pack(side=tk.LEFT, padx=10)

        self.cashout_button = tk.Button(self.controls_frame, text="Cash Out", font=("Arial", 14), bg="#E74C3C", fg="white", command=self.cash_out, state=tk.DISABLED)
        self.cashout_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.controls_frame, text="Reset Game", font=("Arial", 14), bg="#1ABC9C", fg="white", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.create_grid()

    def create_grid(self):
        self.buttons = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = tk.Button(
                    self.grid_frame,
                    width=6,
                    height=3,
                    font=("Arial", 12),
                    bg="#34495E",
                    fg="white",
                    command=lambda x=i, y=j: self.reveal_tile(x, y)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def create_level_section(self):
        for level in range(1, 11):
            button = tk.Button(
                self.level_frame,
                text=f"Level {level}",
                font=("Arial", 12),
                bg="#8E44AD",
                fg="white",
                command=lambda lvl=level: self.select_level(lvl)
            )
            button.pack(pady=5)
            self.level_buttons.append(button)

    def select_level(self, level):
        self.level = level
        self.update_level_label()
        self.reset_board()

    def place_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.money:
                raise ValueError("Invalid bet amount.")
            self.bet = bet
            self.money -= bet
            self.update_money_label()

            self.mines = self.generate_mines()
            self.revealed = []
            self.multiplier = 1.0
            self.cashout_button.config(state=tk.NORMAL)
            self.bet_button.config(state=tk.DISABLED)

            messagebox.showinfo("Game Started", "Bet placed! Click tiles to reveal.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bet amount.")

    def generate_mines(self):
        total_tiles = self.grid_size * self.grid_size
        green_tiles = max(1, total_tiles - self.level)
        mine_tiles = total_tiles - green_tiles

        positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        random.shuffle(positions)
        greens = positions[:green_tiles]
        self.mines = set(positions[green_tiles:])
        return self.mines

    def reveal_tile(self, x, y):
        if (x, y) in self.revealed:
            return

        self.revealed.append((x, y))
        if (x, y) in self.mines:
            self.buttons[x][y].config(text="M", bg="red", fg="white")
            self.end_game(False)
        else:
            self.multiplier += 0.2
            self.buttons[x][y].config(text=f"{self.multiplier:.1f}x", bg="#27AE60", fg="white")

    def cash_out(self):
        winnings = int(self.bet * self.multiplier)
        self.money += winnings
        self.update_money_label()
        messagebox.showinfo("Cash Out", f"You cashed out and won ${winnings}!")
        self.advance_level()

    def end_game(self, won):
        if not won:
            messagebox.showerror("Game Over", "You hit a mine and lost your bet!")
        self.reset_board()

    def reset_board(self):
        self.bet = 0
        self.multiplier = 1.0
        self.cashout_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].config(text="", bg="#34495E", fg="white")

    def reset_game(self):
        self.money = self.starting_money
        self.level = 1
        self.update_money_label()
        self.update_level_label()
        self.reset_board()

    def advance_level(self):
        self.level += 1
        if self.level > 10:
            messagebox.showinfo("Congratulations!", "You have completed all levels!")
            self.reset_game()
        else:
            self.update_level_label()
            self.reset_board()

    def update_money_label(self):
        self.money_label.config(text=f"Money: ${self.money}")

    def update_level_label(self):
        self.level_label.config(text=f"Level: {self.level}")

class OtherGame:
    def __init__(self, root, switch_game_callback):
        self.root = root
        self.switch_game_callback = switch_game_callback
        self.frame = tk.Frame(root, bg="#2C3E50")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(
            self.frame, text="Welcome to the Other Game!", font=("Arial", 24), bg="#2C3E50", fg="white"
        )
        self.label.pack(pady=20)

        self.switch_game_button = tk.Button(
            self.frame, text="Switch to Mines Game", font=("Arial", 14), bg="#1ABC9C", fg="white", command=self.switch_game_callback
        )
        self.switch_game_button.pack(pady=20)

class GameApp:
    def __init__(self, root):
        self.root = root
        self.current_game = None
        self.show_mines_game()

    def show_mines_game(self):
        if self.current_game:
            self.current_game.frame.destroy()
        self.current_game = MinesGame(self.root, self.show_other_game)

    def show_other_game(self):
        if self.current_game:
            self.current_game.frame.destroy()
        self.current_game = OtherGame(self.root, self.show_mines_game)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")
    root.title("Multi-Game App")
    app = GameApp(root)
    root.mainloop()


 

       
   


    
      
        
         
          

           
            
              
               

                 

                  
                   
                    
                      
                       
                        
                          
                           
                            
                             
                              
                               
                                 
                                   
                           


                                
