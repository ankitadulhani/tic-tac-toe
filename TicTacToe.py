from tkinter import *
from tkinter import messagebox
import random

class TIC_TAC_TOE_GAME:
    def __init__(self, root):
        # Basic Initialization
        self.window = root
        self.make_canvas = Canvas(self.window, background="#141414", relief=RAISED, bd=3)
        self.make_canvas.pack(fill=BOTH, expand=1)

        self.machine_cover = []
        self.human_cover = []
        self.prob = []
        self.sign_store = {}
        
        self.chance_counter = 0
        self.technique = -1
        self.game_mode = None  # 'ai' or '2player'
        self.current_player = 'X'  # Track current player for 2-player mode
        
        self.surrounding_store = {1: (2,3,4,7), 2:(1,3), 3:(1,2,6,9), 4:(1,7), 5: (2,4,6,8), 6: (3,9), 7:(1,4,8,9), 8:(7,9), 9:(7,8,6,3)}            

        self.decorating()

    def decorating(self):
        # Game title
        Label(self.make_canvas, text="Tic-Tac-Toe Game", bg="#141414", fg="#ffffff", font=("Lato", 25, "bold")).place(x=110, y=10)
        
        # Status display
        self.status_label = Label(self.make_canvas, text="Select Game Mode", bg="#141414", fg="#FFFFFF", 
                                font=("Arial", 15, "bold"))
        self.status_label.place(x=150, y=50)

        # Turn display
        self.turn_label = Label(self.make_canvas, text="", bg="#141414", fg="#FFFFFF", 
                              font=("Arial", 12))
        self.turn_label.place(x=160, y=370)
        
        # Create game buttons with modern styling
        button_style = {
            'font': ("Arial", 20, "bold"),
            'width': 3,
            'height': 1,
            'bg': "#262626",
            'activebackground': "#ffffff",
            'bd': 3,
            'relief': 'raised'
        }

        # Create 3x3 grid of buttons
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = Button(self.make_canvas, text="", **button_style,
                        command=lambda x=i+1: self.__human_play(x), state=DISABLED)
            btn.place(x=50 + col*120, y=100 + row*100)
            setattr(self, f'btn_{i+1}', btn)

        self.activate_btn = [getattr(self, f'btn_{i}') for i in range(1, 10)]

        # Mode selection buttons with enhanced styling
        button_mode_style = {
            'font': ("Arial", 12, "bold"),
            'bg': "#262626",
            'activebackground': "#ffffff",
            'fg': "#9d9dff",
            'relief': 'raised',
            'bd': 3,
            'width': 10,
            'height': 1
        }

        self.ai_mode_btn = Button(self.make_canvas, text="vs AI", 
                                command=lambda: self.set_game_mode('ai'),
                                **button_mode_style)
        self.ai_mode_btn.place(x=80, y=400)

        self.two_player_btn = Button(self.make_canvas, text="2 Players",
                                   command=lambda: self.set_game_mode('2player'),
                                   **button_mode_style)
        self.two_player_btn.place(x=250, y=400)

        self.reset_btn = Button(self.make_canvas, text="Reset", 
                              command=self.reset, state=DISABLED,
                              **button_mode_style)
        self.reset_btn.place(x=165, y=450)

    def set_game_mode(self, mode):
        self.game_mode = mode
        self.ai_mode_btn.config(state=DISABLED, disabledforeground="grey")
        self.two_player_btn.config(state=DISABLED, disabledforeground="grey")
        self.reset_btn.config(state=NORMAL)
        
        for btn in self.activate_btn:
            btn.config(state=NORMAL)
            
        if mode == 'ai':
            self.status_label.config(text="Playing vs AI")
            self.turn_label.config(text="Your turn (O)")
        else:
            self.status_label.config(text="2 Player Mode")
            self.update_turn_label()

    def update_turn_label(self):
        if self.game_mode == '2player':
            self.turn_label.config(text=f"Player {self.current_player}'s turn")
        elif self.game_mode == 'ai':
            self.turn_label.config(text="Your turn (O)" if self.current_player == 'O' else "AI thinking...")

    def reset(self):
        self.machine_cover.clear()
        self.human_cover.clear()
        self.sign_store.clear()
        self.prob.clear()
        self.technique = -1
        self.chance_counter = 0
        self.current_player = 'X'
        self.game_mode = None
        
        for btn in self.activate_btn:
            btn.config(text="", state=DISABLED)
            
        self.ai_mode_btn.config(state=NORMAL)
        self.two_player_btn.config(state=NORMAL)
        self.reset_btn.config(state=DISABLED)
        
        self.status_label.config(text="Select Game Mode")
        self.turn_label.config(text="")

    def __human_play(self, chance):
        if self.game_mode == 'ai':
            self.chance_counter += 1
            self.__sign_insert(chance, "O")
            self.human_cover.append(chance)
            
            if self.chance_counter == 9:
                self.human_line_match()
            else:
                self.turn_label.config(text="AI thinking...")
                self.window.update()  # Update the display
                self.window.after(500, lambda: self.__machine_play())  # Add a small delay
        else:
            # 2 Player mode logic
            self.chance_counter += 1
            self.__sign_insert(chance, self.current_player)
            
            if self.check_winner(self.current_player):
                self.status_label.config(text=f"Player {self.current_player} wins!")
                self.turn_label.config(text="Game Over!")
                self.game_over_management()
                return
                
            if self.chance_counter == 9:
                self.status_label.config(text="Game Draw!")
                self.turn_label.config(text="Game Over!")
                self.game_over_management()
                return
                
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.update_turn_label()

    def __machine_play(self):
        super_move = self.get_ai_move()  # Get the AI's move (implement this based on your AI logic)
        self.__sign_insert(super_move, "X")
        self.machine_cover.append(super_move)
        
        if self.check_winner('X'):
            self.status_label.config(text="AI wins!")
            self.turn_label.config(text="Game Over!")
            self.game_over_management()
        elif self.chance_counter == 9:
            self.status_label.config(text="Game Draw!")
            self.turn_label.config(text="Game Over!")
            self.game_over_management()
        else:
            self.turn_label.config(text="Your turn (O)")

    def get_ai_move(self):
        # Implement your AI logic here to return the next move
        available_moves = [i+1 for i in range(9) if self.activate_btn[i]['text'] == ""]
        return random.choice(available_moves)

    def check_winner(self, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in win_combinations:
            if all(self.activate_btn[i]['text'] == player for i in combo):
                # Highlight winning combination
                for i in combo:
                    self.activate_btn[i].config(bg="#4CAF50")
                return True
        return False

    def game_over_management(self):
        for btn in self.activate_btn:
            btn.config(state=DISABLED)
        self.reset_btn.config(state=NORMAL)

    def __sign_insert(self, btn_indicator, sign_is):
        button = self.activate_btn[btn_indicator - 1]
        color = "#00FF00" if sign_is == "X" else "red"
        button.config(text=sign_is, state=DISABLED, disabledforeground=color)
        self.sign_store[btn_indicator] = sign_is

if __name__ == "__main__":
    window = Tk()
    window.title("Tic-Tac-Toe Game")
    window.config(bg="#141414")
    window.geometry("450x500")
    window.maxsize(450,500)
    window.minsize(450,500)
    TIC_TAC_TOE_GAME(window)
    window.mainloop()